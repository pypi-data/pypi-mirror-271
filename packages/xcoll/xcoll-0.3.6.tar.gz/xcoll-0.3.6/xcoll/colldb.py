# copyright ############################### #
# This file is part of the Xcoll Package.   #
# Copyright (c) CERN, 2023.                 #
# ######################################### #

import io
import json
import numpy as np
import pandas as pd


#TODO: niet-active collimators op non-active etc (ook crystals)

def load_SixTrack_colldb(filename, *, emit):
    print("Warning: Using 'xcoll.load_SixTrack_colldb()' is deprecated! "
        + "Use 'xcoll.CollimatorDatabase.from_SixTrack()' instead.")
    return CollimatorDatabase.from_SixTrack(file=filename, nemitt_x=emit, nemitt_y=emit)


def _initialise_None(collimator):
    fields = {'s_center':None, 'align_to': None, 's_align_front': None, 's_align_back': None }
    fields.update({'gap_L': None, 'gap_R': None, 'angle_L': 0, 'angle_R': 0, 'offset': 0, 'parking': 1})
    fields.update({'jaw_LU': None, 'jaw_RU': None, 'jaw_LD': None, 'jaw_RD': None, 'family': None, 'overwritten_keys': []})
    fields.update({'side': 'both', 'material': None, 'stage': None, 'collimator_type': None, 'active': True})
    fields.update({'active_length': 0, 'inactive_front': 0, 'inactive_back': 0, 'sigmax': None, 'sigmay': None})
    fields.update({'crystal': None, 'bending_radius': None, 'xdim': 0, 'ydim': 0, 'miscut': 0, 'thick': 0})
    for f, val in fields.items():
        if f not in collimator.keys():
            collimator[f] = val
    for key in collimator.keys():
        if key not in fields.keys():
            raise ValueError(f"Illegal setting {key} in collimator!")


def _dict_keys_to_lower(dct):
    if isinstance(dct, dict):
        return {k.lower(): _dict_keys_to_lower(v) for k,v in dct.items()}
    else:
        return dct


def _get_coll_dct_by_beam(coll, beam):
    # The dictionary can be a CollimatorDatabase for a single beam (beam=None)
    # or for both beams (beam='b1' or beam='b2)
    if beam is not None:
        if isinstance(beam, int) or len(beam) == 1:
            beam = f'b{beam}'
        beam = beam.lower()
    beam_in_db = list(coll.keys())
    
    if beam_in_db == ['b1','b2']:
        if beam is None:
            raise ValueError("Need to specify a beam, because the given dict is for both beams!")
        return coll[beam]

    elif len(beam_in_db) == 1:
        if beam is None:
            beam = beam_in_db[0].lower()
        elif beam != beam_in_db[0].lower():
            raise ValueError("Variable 'beam' does not match beam specified in CollimatorDatabase!")
        return coll[beam]

    elif beam is not None:
        print("Warning: Specified a beam, but the CollimatorDatabase is for a single beam only!")
    return coll


class CollimatorDatabase:

    _init_vars = ['collimator_dict', 'family_dict', 'beam', 'nemitt_x', 'nemitt_y', '_yaml_merged', 'ignore_crystals']
    _init_var_defaults = {'family_dict': {}, 'beam': None, '_yaml_merged': False, 'ignore_crystals': True}

    # -------------------------------
    # ------ Loading functions ------
    # -------------------------------
    
    @classmethod
    def from_yaml(cls, file, **kwargs):

        # Only do the import here, as to not force people to install
        # ruamel if they don't load CollimatorDatabase yaml's
        from ruamel.yaml import YAML
        yaml = YAML(typ='safe')
        if isinstance(file, io.IOBase):
            dct = yaml.load(file)
        else:
            with open(file, 'r') as fid:
                dct = yaml.load(fid)
        dct = _dict_keys_to_lower(dct)

        # If the CollimatorDatabase uses YAML merging, we need a bit of hackery to get the
        # family names from the tags (anchors/aliases)
        _yaml_merged = False
        if 'families' in dct.keys() and not isinstance(dct['families'], dict):
            _yaml_merged = True

            # First we load a round-trip yaml
            yaml = YAML()
            if isinstance(file, io.IOBase):
                full_dct = yaml.load(file)
            else:
                with open(file, 'r') as fid:
                    full_dct = yaml.load(fid)
            famkey = [key for key in full_dct.keys() if key.lower() == 'families'][0]
            collkey = [key for key in full_dct.keys() if key.lower() == 'collimators'][0]
            families = {}

            # We loop over family names to get the name tag ('anchor') of each family
            for fam, full_fam in zip(dct['families'], full_dct[famkey]):
                if full_fam.anchor.value is None:
                    raise ValueError("Missing name tag / anchor in "
                                   + "CollimatorDatabase['families']!")
                # We get the anchor from the rt yaml, and use it as key in the families dict
                families[full_fam.anchor.value.lower()] = {f.lower(): v for f, v in fam.items()}
            dct['families'] = families

            # Now we need to loop over each collimator, and verify which family was used
            beam = kwargs.get('beam', None)
            coll_dct = _get_coll_dct_by_beam(dct['collimators'], beam)
            full_coll_dct = _get_coll_dct_by_beam(full_dct[collkey], beam)
            for coll, full_coll in zip(coll_dct.values(), full_coll_dct.values()):
                if 'family' in coll.keys():
                    raise ValueError(f"Error in {coll}: Cannot use merging for families "
                                    + "and manually specify family as well!")
                elif len(full_coll.merge) > 0:
                    coll['family'] = full_coll.merge[0][1].anchor.value.lower()
                    # Check if some family settings are overwritten for this collimator
                    overwritten_keys = [key.lower() for key in full_coll.keys()
                                        if full_coll._unmerged_contains(key)
                                        and key.lower() in families[coll['family']].keys()]
                    if len(overwritten_keys) > 0:
                        coll['overwritten_keys'] = overwritten_keys
                else:
                    coll['family'] = None

        return cls.from_dict(dct, _yaml_merged=_yaml_merged, **kwargs)


    @classmethod
    def from_json(cls, file, **kwargs):
        if isinstance(file, io.IOBase):
            dct = json.load(file)
        else:
            with open(file, 'r') as fid:
                dct = json.load(fid)
        dct = _dict_keys_to_lower(dct)
        return cls.from_dict(dct, **kwargs)


    @classmethod
    def from_dict(cls, dct, beam=None, _yaml_merged=False, nemitt_x=None, nemitt_y=None, ignore_crystals=True):
        # We make all keys case-insensitive to avoid confusion between different conventions
        # The families are optional
        fam = {}
        dct = _dict_keys_to_lower(dct)

        # Get the emittance
        if nemitt_x is None and nemitt_y is None:
            if 'emittance' not in dct.keys():
                raise ValueError("Missing emittance info! Add 'emittance' as a key to "
                               + "the CollimatorDatabase file, or specify it as 'nemitt_x' "
                               + "and 'nemitt_y' to the loader!")
            nemitt_x = dct['emittance']['x']
            nemitt_y = dct['emittance']['y']
        elif nemitt_x is None or nemitt_y is None:
            raise ValueError("Need to provide both 'nemitt_x' and 'nemitt_y'!")
        elif 'emittance' in dct.keys():
            if dct['emittance']['x'] != nemitt_x or dct['emittance']['y'] != nemitt_y:
                raise ValueError("Emittance in CollimatorDatabase file different from "
                               + "'nemitt_x' and 'nemitt_y'!")

        # Get family and collimator dicts
        if 'families' in dct.keys():
            if not 'collimators' in dct.keys():
                raise ValueError("Could not find 'collimators' dict in CollimatorDatabase!")
            fam  = dct['families']
            coll = dct['collimators']
        elif 'collimators' in dct.keys():
            coll = dct['collimators']
        else:
            coll = dct

        return cls(collimator_dict=coll, family_dict=fam, nemitt_x=nemitt_x, nemitt_y=nemitt_y,
                   beam=beam, _yaml_merged=_yaml_merged, ignore_crystals=ignore_crystals)


    @classmethod
    def from_SixTrack(cls, file, ignore_crystals=True, **kwargs):
        # only import regex here
        import re
        with open(file, 'r') as infile:
            coll_data_string = ''
            family_settings = {}
            family_types = {}
            side = {}
            cry_fields = ['bending_radius', 'xdim', 'ydim', 'thick', 'miscut', 'crystal']
            cry = {}

            for l_no, line in enumerate(infile):
                if line.startswith('#'):
                    continue # Comment
                sline = line.split()
                if len(sline) > 0:
                    if sline[0].lower() == 'nsig_fam':
                        family_settings[sline[1]] = float(sline[2])
                        family_types[sline[1]] = sline[3]
                    elif sline[0].lower() == 'onesided':
                        side[sline[1]] = int(sline[2])
                    elif sline[0].lower() == "crystal":
                        cry[sline[1]] = {}
                        for i, key in enumerate(cry_fields):
                            idx = i+2 if i < 4 else i+3  # we skip "tilt"
                            if i < 5:
                                cry[sline[1]][key] = float(sline[idx])
                            else:
                                cry[sline[1]][key] = int(sline[idx])
                    elif sline[0].lower() == 'settings':
                        pass # Acknowledge and ignore this line
                    elif len(sline) == 6:
                        # Standard collimator definition
                        coll_data_string += line
                    else:
                        print(f"Unknown setting {line}")

        defaults = {}
        _initialise_None(defaults)

        famdct = {key: {'gap': family_settings[key], 'stage': family_types[key]} for key in family_settings}
        names = ['name', 'gap', 'material', 'active_length', 'angle', 'offset']

        df = pd.read_csv(io.StringIO(coll_data_string), sep=r'\s+', index_col=False, names=names)
        df['family'] = df['gap'].copy()
        df['family'] = df['family'].apply(lambda s: None if re.match(r'^-?\d+(\.\d+)?$', str(s)) else s)
        df.insert(5,'stage', df['gap'].apply(lambda s: family_types.get(s, 'UNKNOWN')))

        df['gap'] = df['gap'].apply(lambda s: float(family_settings.get(s, s)))
        # TODO this breaks code if a key has upper case, e.g. gap_L
        df['name'] = df['name'].str.lower() # Make the names lowercase for easy processing
        df['parking'] = 0.025
        if ignore_crystals:
            df = df[~df.name.isin(list(cry.keys()))]
        else:
            for key in cry_fields:
                df[key] = [cry[name][key] if name in cry else defaults[key]
                           for name in df['name']]
            df['crystal'] = ['strip' if s==1 else s for s in df['crystal']]
            df['crystal'] = ['quasi-mosaic' if s==2 else s for s in df['crystal']]
        df['side'] = [side[name] if name in side else defaults['side']
                      for name in df['name']]
        df['side'] = ['both'  if s==0 else s for s in df['side']]
        df['side'] = ['left'  if s==1 else s for s in df['side']]
        df['side'] = ['right' if s==2 else s for s in df['side']]
        df = df.set_index('name')

        return cls.from_dict({'collimators': df.transpose().to_dict(), 'families': famdct}, \
                             ignore_crystals=ignore_crystals, **kwargs)


    def write_to_yaml(self, out, lhc_style=True):
        """
        Writes a colldb in memory to disk in the yaml format.

        > colldb_object.write_to_yaml(<path+name>, lhc_style=Bool)

        if lhc_style == True, it will add comments assuming that the collimators are named
        as in the lhc.

        The function can dump b1, b2 and a general bx, however multi-beam functionality is not yet
        added to the collmanager. TODO

        If any of the dumped keys contains capital letters (e.g. gap_L), it will not be possible
        to load it back into xcoll, since all keys are set to lowercase when importing TODO
        """
        # Dumps collimator database to a YAML file with optional LHC style formatting
        import re

        # Local helper functions
        def _format_dict_entry(key, value, spacing='', mapping=False, key_width=15):
            # Formats a dictionary entry into a string for YAML output
            formatted_values = ',    '.join(f"{k}: {v}" for k, v in value.items())
            formatted_values = re.sub(r'none', 'null', formatted_values, flags=re.IGNORECASE)
            # Ensure key has a fixed width for alignment
            if mapping:
                formatted_key = f'{key}'.ljust(key_width)
            else:
                formatted_key = f'{key}:'.ljust(key_width)
            #formatted_values = formatted_values.ljust(key_width)
            return f"{spacing}{formatted_key} {{ {formatted_values} }}\n"
        
        def _print_values(keys, dct, file, spacing='', mapping=False):
            # Writes formatted dictionary entries to a file
            for key in keys:
                file.write(_format_dict_entry(key, dct[key], spacing=spacing, mapping=mapping))
        
        def _print_colls(colls, dcts, beam, file):
            # Filters and formats collimator data, then writes to a file
            coll_items_to_print = ['<<','gap','angle','material','active','length','side']
            file.write(f'  {beam}:\n')
            for coll in colls:
                coll_dict = dcts._colldb.transpose().to_dict()[coll]
                fam = coll_dict['family']
                fam_keys = []
                if fam is not None:
                    fam_keys = dcts._family_dict[fam].keys()
                    coll_dict = {**{'<<': '*'+fam}, **coll_dict}
                temp_items_to_print = []
                if coll_dict['crystal'] and str(coll_dict['crystal'])!='nan':
                    temp_items_to_print = ['bending_radius','xdim','ydim','miscut','crystal', 'thick']
                if coll_dict['angle_L'] == coll_dict['angle_R']:
                    coll_dict.update({'angle': coll_dict['angle_L']})
                else:
                    temp_items_to_print = temp_items_to_print + ['angle_L','angle_R']
                if coll_dict['gap_L'] == coll_dict['gap_R']:
                    coll_dict.update({'gap': coll_dict['gap_L']})
                elif coll_dict['gap_L'] is None and coll_dict['gap_R'] is not None:
                    coll_dict.update({'gap': coll_dict['gap_R']})
                elif coll_dict['gap_L'] is not None and coll_dict['gap_R'] is None:
                    coll_dict.update({'gap': coll_dict['gap_L']})
                else:
                    temp_items_to_print = temp_items_to_print + ['gap_L','gap_R']
                value = {}
                overwritten_keys = coll_dict['overwritten_keys']
                for key, val in coll_dict.items():
                    if key == 'active_length':
                        key = 'length' 
                    if (key in coll_items_to_print+temp_items_to_print) and (key not in (set(fam_keys)-set(overwritten_keys))) and (val != 'both'):
                        value.update({key: val})
                file.write(_format_dict_entry(coll, value, spacing='    '))
            file.write('\n')   
                                

        LHC_families = ['tcp3', 'tcsg3', 'tcsm3', 'tcla3', 'tcp7', 'tcsg7', 'tcsm7', 'tcla7', 'tcli', 'tdi', 'tcdq', 'tcstcdq', 'tcth1', 'tcth2', 'tcth5', 'tcth8', 'tctv1', 'tctv2', 'tctv5', 'tctv8', 'tclp', 'tcxrp', 'tcryo', 'tcl4', 'tcl5', 'tcl6', 'tct15', 'tct2', 'tct8', 'tcsp', 'tcld']
        with open(f'{out}.yaml', 'w') as file:
            if '_family_dict' in self.__dict__.keys():
                file.write('families:\n')
                if lhc_style:
                    printed_families = []
                    fams_in_dict = self._family_dict.keys()

                    # Momentum cleaning
                    file.write('  # Momentum cleaning\n')
                    sel_fam = [fam for fam in LHC_families if re.match('.*3', fam) and (fam in fams_in_dict)]
                    printed_families += sel_fam
                    _print_values(sel_fam, self._family_dict, file, spacing='  - &', mapping=True)

                    # Betatron cleaning
                    file.write('  # Betatron cleaning\n')
                    sel_fam = [fam for fam in LHC_families if re.match('.*7', fam) and (fam in fams_in_dict)]
                    printed_families += sel_fam
                    _print_values(sel_fam, self._family_dict, file, spacing='  - &', mapping=True)

                    # Injection protection
                    file.write('  # Injection protection\n')
                    sel_fam = [fam for fam in LHC_families if (fam in ['tcli', 'tdi']) and (fam in fams_in_dict)]
                    printed_families += sel_fam
                    _print_values(sel_fam, self._family_dict, file, spacing='  - &', mapping=True)

                    # Dump protection
                    file.write('  # Dump protection\n')
                    sel_fam = [fam for fam in LHC_families if (fam in ['tcdq', 'tcsp', 'tcstcdq']) and (fam in fams_in_dict)]
                    printed_families += sel_fam
                    _print_values(sel_fam, self._family_dict, file, spacing='  - &', mapping=True)

                    # Physics background / debris
                    file.write('  # Physics background / debris\n')
                    sel_fam = [fam for fam in LHC_families if ((re.match('tc[lt][0-9dp].*', fam)) or (fam in ['tcryo', 'tcxrp'])) and (fam in fams_in_dict)]
                    printed_families += sel_fam
                    _print_values(sel_fam, self._family_dict, file, spacing='  - &', mapping=True)

                    # Other families
                    if set(printed_families) != set(fams_in_dict):
                        file.write('  # Other families\n')
                        _print_values(set(fams_in_dict) - set(printed_families), self._family_dict, file, spacing='  - &', mapping=True)
                else:
                    file.write('  # Families\n')
                    _print_values(self._family_dict.keys(), self._family_dict, file, spacing='  - &', mapping=True)

            # Emittance section
            ex = self.emittance[0]
            ey = self.emittance[1]
            file.write(f'\nemittance:\n  x: {ex}\n  y: {ey}\n')

            # Collimators section
            file.write('\ncollimators:\n')
            b1_colls, b2_colls, bx_colls = [], [], []
            for coll in self._colldb.index:
                if coll == 'tclia.4r2' or coll == 'tclia.4l8':
                    b1_colls.append(coll)
                    b2_colls.append(coll)
                elif coll[-2:] == 'b1':
                    b1_colls.append(coll)
                elif coll[-2:] == 'b2':
                    b2_colls.append(coll)
                else:
                    bx_colls.append(coll)
            
            # Handle special cases for collimators
            if (('tclia.4r2' in b1_colls) or ('tclia.4l8' in b1_colls)) and (len(b1_colls) <= 2):
                b1_colls = []
            if (('tclia.4r2' in b2_colls) or ('tclia.4l8' in b2_colls)) and (len(b2_colls) <= 2):
                b2_colls = []

            # Print collimators for each beam
            if len(b1_colls) > 0:
                _print_colls(b1_colls, self, 'b1', file)
            if len(b2_colls) > 0:
                _print_colls(b2_colls, self, 'b2', file)
            if len(bx_colls) > 0:
                _print_colls(bx_colls, self, 'bx', file)
                print('WARNING -- some collimators could not be assigned to b1 or b2. Tracking might not work with those collimators. Please manually change the output file if necessary.')


    def __init__(self, **kwargs):
        # Get all arguments
        for var in self._init_vars:
            if var in self._init_var_defaults:
                kwargs.setdefault(var, self._init_var_defaults[var])
            elif var not in kwargs.keys():
                raise ValueError(f"CollimatorDatabase is missing required argument '{var}'!")

        self._optics = pd.DataFrame(columns=['x', 'px', 'y', 'py', 'betx', 'bety', 'alfx', 'alfy', 'dx', 'dy'])
        self._parse_dict(kwargs['collimator_dict'], kwargs['family_dict'],
                         kwargs['beam'], kwargs['_yaml_merged'], kwargs.get('ignore_crystals', True))
        self.emittance = [kwargs['nemitt_x'], kwargs['nemitt_y']]
        self._beta_gamma_rel = None


    def __getitem__(self, name):
        return CollimatorSettings(name, self._colldb)

    def to_pandas(self):
        return pd.DataFrame({
                's_center':        self.s_center,
                'gap':             self.gap,
                'jaw':             self.jaw,
                'beam_size':       self.beam_size,
                'aligned_to':      self.align_to,
                'angle':           self.angle,
                'material':        self.material,
#                 'offset':          self.offset,
#                 'tilt':            self.tilt,
                'stage':           self.stage,
                'active_length':   self.active_length,
                'collimator_type': self.collimator_type,
            }, index=self.name)


    def _parse_dict(self, coll, fam, beam=None, _yaml_merged=False, ignore_crystals=True):

        # We make all keys case-insensitive to avoid confusion between different conventions
        coll = _dict_keys_to_lower(coll)
        fam  = _dict_keys_to_lower(fam)

        # The dictionary can be a CollimatorDatabase for a single beam (beam=None)
        # or for both beams (beam='b1' or beam='b2)
        coll = _get_coll_dct_by_beam(coll, beam)

        # Apply family settings
        crystals = []
        for thiscoll, settings in coll.items():
            settings = {k.lower(): v for k,v in settings.items()}
            if 'family' in settings.keys() and settings['family'] is not None:
                settings['family'] = settings['family'].lower()
                thisfam = settings['family']
                if thisfam not in fam.keys():
                    raise ValueError(f"Collimator {thiscoll} depends on family {thisfam}, "
                                   + f"but the latter is not defined!")

                # Check if some family settings are overwritten for this collimator
                # Only do this check if we didn't do a YAML merge earlier (because then it
                # is already taken care of)
                if not _yaml_merged:
                    overwritten_keys = [key.lower() for key in settings.keys() if key in fam[thisfam]]
                    if len(overwritten_keys) > 0:
                        settings['overwritten_keys'] = overwritten_keys

                # Load family settings, potentially overwriting settings for this collimator
                settings = {**fam[thisfam], **settings}

            else:
                settings['family'] = None
            coll[thiscoll] = settings

            # Save list of crystals
            if 'crystal' in settings:
                if settings['crystal'] != 0.0:
                    crystals += [thiscoll]
                else: 
                    settings['crystal'] = None

        # Remove crystals from colldb
        if ignore_crystals:
            for thiscoll in crystals:
                del coll[thiscoll]

        # Check that all collimators have gap settings
        if not np.all(['gap' in val.keys() or 'opening' in val.keys() for val in coll.values()]):
            raise ValueError("Ill-defined CollimatorDatabase: Not all collimators have a gap or "
                           + "opening setting, (or the keys / structure of the dictionary is wrong)!")

        # Update collimators with default values for missing keys
        for collimator in coll.values():
            # Change all values to lower case
            for key, val in collimator.items():
                collimator[key] = val.lower() if isinstance(val, str) else val
            if 'length' in collimator.keys():
                collimator['active_length'] = collimator.pop('length')
            if 'gap' in collimator.keys():
                if collimator['gap'] is not None and collimator['gap'] > 900:
                    collimator['gap'] = None
                if 'side' in collimator.keys() and collimator['side'] == 'left':
                    collimator['gap_L'] = collimator.pop('gap')
                    collimator['gap_R'] = None
                elif 'side' in collimator.keys() and collimator['side'] == 'right':
                    collimator['gap_L'] = None
                    collimator['gap_R'] = collimator.pop('gap')
                else:
                    collimator['gap_L'] = collimator['gap']
                    collimator['gap_R'] = collimator.pop('gap')
            if 'angle' in collimator.keys():
                collimator['angle_L'] = collimator['angle']
                collimator['angle_R'] = collimator.pop('angle')
            _initialise_None(collimator)

        self._collimator_dict = coll
        self._family_dict = fam
        self._colldb = pd.DataFrame(coll).transpose()


    @property
    def name(self):
        return self._colldb.index.values


    # TODO: - VALIDATION OF TYPES (e.g. material, stage, align, ..)
    #       - IMPLEMENTATION OF TILT
    #       - CRYSTAL PROPERTIES: only valid if crystal == True (add mask to _set_property?)
    #         make second dataframe for crystals
    #       - show as __repr__

    # The CollimatorDatabase class has the following fields (those marked
    # with an * are set automatically and cannot be overwritten):
    #   - name
    #   - gap
    #   - jaw *
    #   - beam_size *
    #   - s_center *
    #   - angle
    #   - material
    #   - offset
    #   - tilt
    #   - stage
    #   - side
    #   - active_length
    #   - inactive_front
    #   - inactive_back
    #   - total_length *
    #   - collimator_type *
    #   - betx
    #   - bety
    #   - x
    #   - px
    #   - y
    #   - py
    #   - gamma_rel
    #   - emit

    @property
    def angle(self):
#         angles = np.array([self._colldb.angle_L.values,self._colldb.angle_R.values])
#         return pd.Series([ L if L == R else [L,R] for L, R in angles.T ], index=self._colldb.index, dtype=object)
        return self._colldb['angle_L']

    @angle.setter
    def angle(self, angle):
        self._set_property_LR('angle', angle)
        self._compute_jaws()

    @property
    def material(self):
        return self._colldb['material']

    @material.setter
    def material(self, material):
        self._set_property('material', material)

    @property
    def offset(self):
        return self._colldb['offset']

    @offset.setter
    def offset(self, offset):
        self._set_property('offset', offset, single_default_allowed=True)
        self._compute_jaws()

    @property
    def tilt(self):
        tilts = np.array([self._colldb.tilt_L.values,self._colldb.tilt_R.values])
        return pd.Series([ L if L == R else [L,R] for L, R in tilts.T ], index=self._colldb.index, dtype=object)

    @tilt.setter
    def tilt(self, tilts):
        self._set_property_LR('tilt', tilts)
        self._compute_jaws()

    @property
    def stage(self):
        return self._colldb['stage']

    @stage.setter
    def stage(self, stage):
        self._set_property('stage', stage)

    @property
    def parking(self):
        return self._colldb['parking']

    @parking.setter
    def parking(self, parking):
        self._set_property('parking', parking, single_default_allowed=True)
        self._compute_jaws()

    @property
    def active(self):
        return self._colldb['active']

    @active.setter
    def active(self, active):
        self._set_property('active', active, single_default_allowed=True)

#     @property
#     def crystal(self):
#         return self._colldb['crystal']

#     @crystal.setter
#     def crystal(self, crystal):
#         self._set_property('crystal', crystal)

#     @property
#     def bend(self):
#         return self._colldb['bend']

#     @bend.setter
#     def bend(self, bend):
#         self._set_property('bend', bend)

#     @property
#     def xdim(self):
#         return self._colldb['xdim']

#     @xdim.setter
#     def xdim(self, xdim):
#         self._set_property('xdim', xdim)

#     @property
#     def ydim(self):
#         return self._colldb['ydim']

#     @ydim.setter
#     def ydim(self, ydim):
#         self._set_property('ydim', ydim)

#     @property
#     def miscut(self):
#         return self._colldb['miscut']

#     @miscut.setter
#     def miscut(self, miscut):
#         self._set_property('miscut', miscut)

#     @property
#     def thick(self):
#         return self._colldb['thick']

#     @thick.setter
#     def thick(self, thick):
#         self._set_property('thick', thick)

    @property
    def s_center(self):
        return self._colldb['s_center']

    @property
    def collimator_type(self):
        return self._colldb['collimator_type']

    @property
    def active_length(self):
        return self._colldb['active_length']

    @active_length.setter
    def active_length(self, length):
        self._set_property('active_length', length)
        self.align_to = {}

    @property
    def inactive_front(self):
        return self._colldb['inactive_front']

    @inactive_front.setter
    def inactive_front(self, length):
        self._set_property('inactive_front', length)

    @property
    def inactive_back(self):
        return self._colldb['inactive_back']

    @inactive_back.setter
    def inactive_back(self, length):
        self._set_property('inactive_back', length)

    @property
    def total_length(self):
        return self._colldb['active_length'] +  self._colldb['inactive_front'] + self._colldb['inactive_back']

    @property
    def gap(self):
        gaps = np.array([self._colldb.gap_L.values,self._colldb.gap_R.values])
        return pd.Series([ L if L == R else [L,R] for L, R in gaps.T ], index=self._colldb.index, dtype=object)

    @gap.setter
    def gap(self, gaps):
        df = self._colldb
        correct_format = False
        # The variable gaps is a Series or a list
        if isinstance(gaps, pd.Series) or isinstance(gaps, list) or isinstance(gaps, np.ndarray):
            correct_format = True
            if len(gaps) != len(self.name):
                raise ValueError("The variable 'gaps' has a different length than the number "
                                + "of collimators in the CollimatorDatabase. Use a dictionary instead.")
            # Some of the gaps are list (e.g. two different values for both gaps): loop over gaps as dict
            if any(hasattr(gap, '__iter__') for gap in gaps):
                gaps = dict(zip(self.name, gaps))
            # All gaps are single values: use pandas-style assignment
            else:
                # mask those that have an active side for the gap under consideration
                # and have a setting less than 900; the others are set to None
                mask_L = np.logical_and(df.side.isin(['both','left']), ~(gaps >= 900))
                mask_R = np.logical_and(df.side.isin(['both','right']), ~(gaps >= 900))
                df.loc[mask_L, 'gap_L'] = gaps[mask_L]
                df.loc[~mask_L, 'gap_L'] = None
                df.loc[mask_R, 'gap_R'] = gaps[mask_R]
                df.loc[~mask_R, 'gap_R'] = None

        # The variable gaps is a dictionary
        if isinstance(gaps, dict):
            correct_format = True
            for name, gap in gaps.items():
                if name not in self.name:
                    raise ValueError(f"Collimator {name} not found in CollimatorDatabase!")
                side = df.side[name]
                if hasattr(gap, '__iter__'):
                    if isinstance(gap, str):
                        raise ValueError("The gap setting has to be a number!")
                    elif len(gap) == 2:
                        gap_L = gap[0]
                        gap_R = gap[1]
                        if side != 'both':
                            if side == 'left' and gap_R is not None:
                                print(f"Warning: collimator {name} is left-sided but a finite right gap is specified. "
                                      + "Verify that this is what you want.")
                            elif side == 'right' and gap_L is not None:
                                print(f"Warning: collimator {name} is right-sided but a finite left gap is specified. "
                                      + "Verify that this is what you want.")
                    elif len(gap) == 1:
                        gap_L = gap[0] if side in ['both','left'] else None
                        gap_R = gap[0] if side in ['both','right'] else None
                    else:
                        raise ValueError("The gap setting must have one or two values (for the left and the right jaw)!")
                else:
                    gap_L = gap if side in ['both','left'] else None
                    gap_R = gap if side in ['both','right'] else None
                gap_L = None if (gap_L is not None and gap_L >= 900) else gap_L
                gap_R = None if (gap_R is not None and gap_R >= 900) else gap_R
                df.loc[name, 'gap_L'] = gap_L
                df.loc[name, 'gap_R'] = gap_R

        if not correct_format:
            raise ValueError("Variable 'gaps' needs to be a pandas Series, dict, numpy array, or list!")

        df.gap_L = df.gap_L.astype('object', copy=False)
        df.gap_R = df.gap_R.astype('object', copy=False)
        self._compute_jaws()

    @property
    def jaw(self):
        jaws = list(np.array([
                        self._colldb.jaw_LU.values,
                        self._colldb.jaw_RU.values,
                        self._colldb.jaw_LD.values,
                        self._colldb.jaw_RD.values
                    ]).T)
        # Need special treatment if there are None's
        def flip(jaw):
            return None if jaw is None else -jaw
        for i, jaw in enumerate(jaws):
            # All 4 jaw points are the same
            if jaw[0] == flip(jaw[1]) == jaw[2] == flip(jaw[3]):
                jaws[i] = jaw[0]
            # Upstream and downstream jaws are the same
            # (all cases except angular alignment and/or tilt)
            elif jaw[0] == jaw[2] and jaw[1] == jaw[3]:
                jaws[i] = [ jaw[0], jaw[1] ]
            else:
                jaws[i] = [ [jaw[0],jaw[1]], [jaw[2],jaw[3]] ]
        return pd.Series(jaws, index=self._colldb.index, dtype=object)

    @property
    def side(self):
        return self._colldb.side

    @side.setter
    def side(self, sides):
        self._set_property('side', sides, single_default_allowed=True)
        self.gap = self.gap

    @property
    def gamma_rel(self):
        return np.sqrt(self._beta_gamma_rel**2+1)

    @gamma_rel.setter
    def gamma_rel(self, gamma_rel):
        self._beta_gamma_rel = np.sqrt(gamma_rel**2-1)
        self._compute_jaws()

    @property
    def emittance(self):
        return [self._emitx, self._emity]

    @emittance.setter
    def emittance(self, emit):
        if hasattr(emit, '__iter__'):
            if isinstance(emit, str):
                raise ValueError(f"The 'emit' setting has to be a number!")
            elif len(emit) == 2:
                self._emitx = emit[0]
                self._emity = emit[1]
            elif len(emit) == 1:
                self._emitx = emit[0]
                self._emity = emit[0]
            else:
                raise ValueError(f"The 'emit' setting must have one or two values (for emitx and emity)!")
        else:
            self._emitx = emit
            self._emity = emit
        self._compute_jaws()

    @property
    def align_to(self):
        return self._colldb.align_to

    @align_to.setter
    def align_to(self, align):
        self._set_property('align_to', align, single_default_allowed=True, limit_to=['front', 'center', 'back', 'angular'])
        if np.any(self.align_to == 'maximum'):
            raise NotImplementedError
        s_front = self.s_center - self.active_length/2
        s_center = self.s_center
        s_back = self.s_center + self.active_length/2
        mask = self.align_to == 'front'
        self._colldb.loc[mask,'s_align_front'] = s_front[mask]
        self._colldb.loc[mask,'s_align_back']  = s_front[mask]
        mask = self.align_to == 'center'
        self._colldb.loc[mask,'s_align_front'] = s_center[mask]
        self._colldb.loc[mask,'s_align_back']  = s_center[mask]
        mask = self.align_to == 'back'
        self._colldb.loc[mask,'s_align_front'] = s_back[mask]
        self._colldb.loc[mask,'s_align_back']  = s_back[mask]
        mask = self.align_to == 'angular'
        self._colldb.loc[mask,'s_align_front'] = s_front[mask]
        self._colldb.loc[mask,'s_align_back']  = s_back[mask]
        self._compute_jaws()

    # TODO: when does this need to be unset?
    @property
    def _optics_is_ready(self):
        pos = set(self._colldb.s_align_front.values) | set(self._colldb.s_align_back.values)
        return np.all([s in self._optics.index for s in pos]) and self._beta_gamma_rel is not None

    @property
    def betx(self):
        vals = np.array([
            [ self._optics.loc[s,'betx'] if s in self._optics.index else None for s in self._colldb.s_align_front.values ],
            [ self._optics.loc[s,'betx'] if s in self._optics.index else None for s in self._colldb.s_align_back.values ]
        ])
        return pd.Series([ F if F == B else [F,B] for F,B in vals.T ], index=self._colldb.index, dtype=object)

    @property
    def bety(self):
        vals = np.array([
            [ self._optics.loc[s,'bety'] if s in self._optics.index else None for s in self._colldb.s_align_front.values ],
            [ self._optics.loc[s,'bety'] if s in self._optics.index else None for s in self._colldb.s_align_back.values ]
        ])
        return pd.Series([ F if F == B else [F,B] for F,B in vals.T ], index=self._colldb.index, dtype=object)

    @property
    def alfx(self):
        vals = np.array([
            [ self._optics.loc[s,'alfx'] if s in self._optics.index else None for s in self._colldb.s_align_front.values ],
            [ self._optics.loc[s,'alfx'] if s in self._optics.index else None for s in self._colldb.s_align_back.values ]
        ])
        return pd.Series([ F if F == B else [F,B] for F,B in vals.T ], index=self._colldb.index, dtype=object)   

    @property
    def alfy(self):
        vals = np.array([
            [ self._optics.loc[s,'alfy'] if s in self._optics.index else None for s in self._colldb.s_align_front.values ],
            [ self._optics.loc[s,'alfy'] if s in self._optics.index else None for s in self._colldb.s_align_back.values ]
        ])
        return pd.Series([ F if F == B else [F,B] for F,B in vals.T ], index=self._colldb.index, dtype=object)
    
    @property
    def dx(self):
        vals = np.array([
            [ self._optics.loc[s,'dx'] if s in self._optics.index else None for s in self._colldb.s_align_front.values ],
            [ self._optics.loc[s,'dx'] if s in self._optics.index else None for s in self._colldb.s_align_back.values ]
        ])
        return pd.Series([ F if F == B else [F,B] for F,B in vals.T ], index=self._colldb.index, dtype=object)

    @property
    def dy(self):
        vals = np.array([
            [ self._optics.loc[s,'dy'] if s in self._optics.index else None for s in self._colldb.s_align_front.values ],
            [ self._optics.loc[s,'dy'] if s in self._optics.index else None for s in self._colldb.s_align_back.values ]
        ])
        return pd.Series([ F if F == B else [F,B] for F,B in vals.T ], index=self._colldb.index, dtype=object)
    
    @property
    def x(self):
        vals = np.array([
            [ self._optics.loc[s,'x'] if s in self._optics.index else None for s in self._colldb.s_align_front.values ],
            [ self._optics.loc[s,'x'] if s in self._optics.index else None for s in self._colldb.s_align_back.values ]
        ])
        return pd.Series([ F if F == B else [F,B] for F,B in vals.T ], index=self._colldb.index, dtype=object)

    @property
    def px(self):
        vals = np.array([
            [ self._optics.loc[s,'px'] if s in self._optics.index else None for s in self._colldb.s_align_front.values ],
            [ self._optics.loc[s,'px'] if s in self._optics.index else None for s in self._colldb.s_align_back.values ]
        ])
        return pd.Series([ F if F == B else [F,B] for F,B in vals.T ], index=self._colldb.index, dtype=object)

    @property
    def y(self):
        vals = np.array([
            [ self._optics.loc[s,'y'] if s in self._optics.index else None for s in self._colldb.s_align_front.values ],
            [ self._optics.loc[s,'y'] if s in self._optics.index else None for s in self._colldb.s_align_back.values ]
        ])
        return pd.Series([ F if F == B else [F,B] for F,B in vals.T ], index=self._colldb.index, dtype=object)

    @property
    def py(self):
        vals = np.array([
            [ self._optics.loc[s,'py'] if s in self._optics.index else None for s in self._colldb.s_align_front.values ],
            [ self._optics.loc[s,'py'] if s in self._optics.index else None for s in self._colldb.s_align_back.values ]
        ])
        return pd.Series([ F if F == B else [F,B] for F,B in vals.T ], index=self._colldb.index, dtype=object)

    @property
    def beam_size(self):
        if self._optics_is_ready:
            beam_size = np.array([self._beam_size_front,self._beam_size_back])
            return pd.Series([ F if F == B else [F,B] for F, B in beam_size.T ], index=self._colldb.index, dtype=object)
        else:
            return None

    @property
    def _beam_size_front(self):
        # TODO: curretnly only for angle_L
        df = self._colldb
        opt = self._optics
        betx = opt.loc[df.s_align_front,'betx'].astype(float)
        bety = opt.loc[df.s_align_front,'bety'].astype(float)
        sigmax = np.sqrt(betx*self._emitx/self._beta_gamma_rel)
        sigmay = np.sqrt(bety*self._emity/self._beta_gamma_rel)
        result = np.sqrt(
                    (sigmax*np.cos(np.float_(df.angle_L.values)*np.pi/180))**2
                    + (sigmay*np.sin(np.float_(df.angle_L.values)*np.pi/180))**2
                )
        result.index = self._colldb.index
        return result

    @property
    def _beam_size_back(self):
        # TODO: curretnly only for angle_L
        df = self._colldb
        opt = self._optics
        betx = opt.loc[df.s_align_back,'betx'].astype(float)
        bety = opt.loc[df.s_align_back,'bety'].astype(float)
        sigmax = np.sqrt(betx*self._emitx/self._beta_gamma_rel)
        sigmay = np.sqrt(bety*self._emity/self._beta_gamma_rel)
        result = np.sqrt(
                    (sigmax*np.cos(np.float_(df.angle_L.values)*np.pi/180))**2
                    + (sigmay*np.sin(np.float_(df.angle_L.values)*np.pi/180))**2
                )
        result.index = self._colldb.index
        return result

    # parking is defined with respect to closed orbit
    # TODO: tilt
    # 'upstr'  =>  'front'  en   'downstr'  =>  'back'
    def _compute_jaws(self):
        if self._optics_is_ready:
            df = self._colldb
            beam_size_front = self._beam_size_front
            beam_size_back  = self._beam_size_back
            jaw_LU = df['gap_L']*beam_size_front + self.offset
            jaw_RU = df['gap_R']*beam_size_front - self.offset
            jaw_LD = df['gap_L']*beam_size_back  + self.offset
            jaw_RD = df['gap_R']*beam_size_back  - self.offset
            df['jaw_LU'] = df['parking'] if df['gap_L'] is None else np.minimum(jaw_LU,df['parking'])
            df['jaw_RU'] = -df['parking'] if df['gap_R'] is None else -np.minimum(jaw_RU,df['parking'])
            df['jaw_LD'] = df['parking'] if df['gap_L'] is None else np.minimum(jaw_LD,df['parking'])
            df['jaw_RD'] = -df['parking'] if df['gap_R'] is None else -np.minimum(jaw_RD,df['parking'])
            # align crystals
            opt = self._optics
            df['align_angle'] = None
            cry_mask = [c is not None for c in df.crystal]
            df_cry = df[cry_mask]
            if len(df_cry) > 0:
                alfx = opt.loc[df_cry.s_align_front,'alfx'].astype(float).values
                alfy = opt.loc[df_cry.s_align_front,'alfy'].astype(float).values
                betx = opt.loc[df_cry.s_align_front,'betx'].astype(float).values
                bety = opt.loc[df_cry.s_align_front,'bety'].astype(float).values
                align_angle_x = -np.sqrt(self._emitx/self._beta_gamma_rel/betx)*alfx
                align_angle_y = -np.sqrt(self._emity/self._beta_gamma_rel/bety)*alfy
                align_angle = np.array([x if abs(ang) < 1e-6 else y
                                        for x,y,ang in zip(align_angle_x,align_angle_y,df_cry.angle_L.values)])
                df.loc[cry_mask, 'align_angle'] = align_angle*df_cry['gap_L']


    # ---------------------------------------
    # ------ Property setter functions ------
    # ---------------------------------------

    def _set_property(self, prop, vals, single_default_allowed=False, limit_to=[]):
        df = self._colldb
        if not isinstance(limit_to, (list, tuple, set)):
            limit_to = [limit_to]
        if isinstance(vals, dict):
            for name, val in vals.items():
                if name not in self.name:
                    raise ValueError(f"Collimator {name} not found in CollimatorDatabase!")
                if limit_to!=[] and val not in limit_to:
                    raise ValueError(f"Cannot set {prop} to {val}. Choose from {limit_to}!")
                df.loc[name, prop] = val
        elif isinstance(vals, pd.Series) or isinstance(vals, list) or isinstance(vals, np.ndarray):
            if len(vals) != len(self.name):
                raise ValueError(f"The variable '{prop}' has a different length than the number of "
                                + "collimators in the CollimatorDatabase. Use a dictionary instead.")
            if limit_to!=[] and np.any([val not in limit_to for val in vals]):
                raise ValueError(f"Cannot set {prop} to {vals}. Choose from {limit_to}!")
            df[prop] = vals
        else:
            if single_default_allowed:
                if limit_to!=[] and vals not in limit_to:
                    raise ValueError(f"Cannot set {prop} to {vals}. Choose from {limit_to}!")
                df[prop] = vals
            else:
                raise ValueError(f"Variable '{prop}' needs to be a pandas Series, dict, numpy array, or list!")


    def _set_property_LR(self, prop, vals):
        df = self._colldb
        correct_format = False
        # The variable vals is a Series or a list
        if isinstance(vals, pd.Series) or isinstance(vals, list) or isinstance(vals, np.ndarray):
            correct_format = True
            if len(vals) != len(self.name):
                raise ValueError(f"The variable '{prop}' has a different length than the number of "
                                + "collimators in the CollimatorDatabase. Use a dictionary instead.")
            # Some of the vals are list (e.g. two different values for both gaps): loop over vals as dict
            if any(hasattr(val, '__iter__') for val in vals):
                vals = dict(zip(self.name, vals))
            # All gaps are single values: use pandas-style assignment
            else:
                df[prop + "_L"] = vals
                df[prop + "_R"] = vals
        
        # The variable vals is a dictionary
        if isinstance(vals, dict):
            correct_format = True
            for name, val in vals.items():
                if name not in self.name:
                    raise ValueError(f"Collimator {name} not found in CollimatorDatabase!")
                if hasattr(val, '__iter__'):
                    if isinstance(val, str):
                        raise ValueError(f"The '{prop}' setting has to be a number!")
                    elif len(val) == 2:
                        val_L = val[0]
                        val_R = val[1]
                    elif len(val) == 1:
                        val_L = val[0]
                        val_R = val[0]
                    else:
                        raise ValueError(f"The '{prop}' setting must have one or two values (for the left and the right jaw)!")
                else:
                    val_L = val
                    val_R = val
                df.loc[name, prop + "_L"] = val_L
                df.loc[name, prop + "_R"] = val_R

        if not correct_format:
            raise ValueError("Variable '{prop}' needs to be a pandas Series, dict, numpy array, or list!")

        df[prop + "_L"] = df[prop + "_L"].astype('object', copy=False)
        df[prop + "_R"] = df[prop + "_R"].astype('object', copy=False)
        # Check if collimator active
        # Check if gap is list (assymetric jaws)
