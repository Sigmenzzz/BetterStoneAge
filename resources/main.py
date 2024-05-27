import json

from alcs_funcs import *
from mcresources.resource_manager import ResourceManager, utils

rm = ResourceManager('better_stone_age', 'src/main/resources', 2, False, 'en_us')
tfc_rm = ResourceManager('tfc', 'src/main/resources', 2, False, 'en_us')
forge_rm = ResourceManager('forge', 'src/main/resources', 2, False, 'en_us')
STONE_TOOL_HEADS = ('hammer', 'hoe', 'javelin', 'knife', 'shovel', 'axe')
STONE_TOOL_BINDINGS = ('weak', 'medium', 'strong')
BINDING_BONUSES = {'weak': 0, 'medium': 2, 'strong': 4}
ROCK_CATEGORY_DURABILITIES = {'igneous_extrusive': 70, 'igneous_intrusive': 60, 'metamorphic': 55, 'sedimentary': 50}
with open('templates/pot_model.json', 'r') as f:
    pot_template = f.read()

def loot_modifier_add_itemstack(rm: ResourceManager, loot_modifiers: list, name_parts, entity_tag, item, count):
    
    
    data = {
      "type": "better_stone_age:add_itemstack",
      "conditions": [
        {
          "condition": "minecraft:entity_properties",
          "predicate": {
              "type": entity_tag
          },
          "entity": "this"
        }
      ],
      "item": item,
      "count": count
    }
    
    loot_modifier(rm, loot_modifiers, name_parts, data)

def loot_modifier_add_itemstack_min_max(rm: ResourceManager, loot_modifiers: list, name_parts, entity_tag, item, little, big):
    
    
    data = {
      "type": "better_stone_age:add_itemstack_min_max",
      "conditions": [
        {
          "condition": "minecraft:entity_properties",
          "predicate": {
              "type": entity_tag
          },
          "entity": "this"
        }
      ],
      "item": item,
      "min": little,
      "max": big
    }
    
    loot_modifier(rm, loot_modifiers, name_parts, data)
    
    
def loot_modifier(rm: ResourceManager, loot_modifiers: list, name_parts, data):

    if isinstance(name_parts, str):
        name_parts = [name_parts]
    
    rm.data(['loot_modifiers'] + name_parts, data)
    
    loot_modifiers.append(f'better_stone_age:{"/".join(name_parts)}')
    
    
def create_anvil_recipes():
    print('\tCreating anvil recipes...')
    anvil_recipe(rm, ('pounded_sinew'), 'better_stone_age:dried_sinew', 'better_stone_age:pounded_sinew', Rules.hit_third_last, Rules.hit_second_last, Rules.hit_last)

def create_barrel_recipes():
    print('\tCreating barrel recipes...')
    for color in COLORS:
        barrel_sealed_recipe(rm, ('ceramic', 'jug', 'unfired', color), f'Dyeing Unfired Jug {color}', 1000, 'tfc:ceramic/unfired_jug', f'25 tfc:{color}_dye', f'better_stone_age:ceramic/jug/unfired/{color}')
    
def create_crafting_recipes():
    print('\tCreating crafting recipes...')
    
    print('\t\tCreating color recipes...')
    for color in COLORS:
        rm.crafting_shapeless(('crafting', 'ceramic', 'jug', 'unfired' f'{color}'), ('tfc:ceramic/unfired_jug', f'minecraft:{color.lower()}_dye'), f'better_stone_age:ceramic/jug/unfired/{color}')
        rm.crafting_shapeless(('crafting', 'ceramic', 'jug', 'unfired' f'{color}_liquid_dye'), ('tfc:ceramic/unfired_jug', fluid_item_ingredient(f'100 tfc:{color}_dye')), f'better_stone_age:ceramic/jug/unfired/{color}')
        rm.crafting_shapeless(('crafting', 'ceramic', f'{color}_unfired_vessel_liquid_dye'), ('tfc:ceramic/unfired_vessel', fluid_item_ingredient(f'100 tfc:{color}_dye')), f'tfc:ceramic/{color}_unfired_vessel')
        rm.crafting_shapeless(('crafting', 'ceramic', f'{color}_unfired_large_vessel_liquid_dye'), ('tfc:ceramic/unfired_large_vessel', fluid_item_ingredient(f'100 tfc:{color}_dye')), f'tfc:ceramic/unfired_large_vessel/{color}')
    
    rm.crafting_shapeless(('crafting', 'dye', 'darken_blue'), ('minecraft:light_blue_dye', 'minecraft:black_dye'), utils.item_stack({'item': 'minecraft:blue_dye', 'count': 2}))
    rm.crafting_shapeless(('crafting', 'dye', 'darken_gray'), ('minecraft:light_gray_dye', 'minecraft:black_dye'), utils.item_stack({'item': 'minecraft:gray_dye', 'count': 2}))
    rm.crafting_shapeless(('crafting', 'dye', 'darken_green'), ('minecraft:lime_dye', 'minecraft:black_dye'), utils.item_stack({'item': 'minecraft:green_dye', 'count': 2}))
    rm.crafting_shapeless(('crafting', 'dye', 'darken_purple'), ('minecraft:magenta_dye', 'minecraft:black_dye'), utils.item_stack({'item': 'minecraft:purple_dye', 'count': 2}))
    
    rm.crafting_shapeless(('crafting', 'dye', 'white_from_flux'), 'tfc:powder/flux', 'minecraft:white_dye')
    rm.crafting_shapeless('crafting', 'better_stone_age:pounded_sinew', 'better_stone_age:sinew_string')
    
    print('\t\tCreating rock category-dependant recipes...')
    for rock_category in ROCK_CATEGORIES:
        for tool_type in STONE_TOOL_HEADS:
            rm.crafting_shaped(('crafting', 'stone', tool_type, rock_category, 'no_binding'), ['H', 'R'], {'H': f'tfc:stone/{tool_type}_head/{rock_category}', 'R': '#forge:rods/wooden'}, utils.item_stack({'item': f'tfc:stone/{tool_type}/{rock_category}', 'nbt': {'Damage': ROCK_CATEGORY_DURABILITIES[rock_category] // 2}}))
            disable_recipe(rm, f'tfc:crafting/stone/{tool_type}_{rock_category}')
            
            for binding in STONE_TOOL_BINDINGS:
                rm.crafting_shaped(('crafting', 'stone', tool_type, rock_category, f'{binding}_binding'), ['BH', 'R '], {'B': f'#better_stone_age:bindings/{binding}', 'H': f'tfc:stone/{tool_type}_head/{rock_category}', 'R': '#forge:rods/wooden'}, utils.item_stack(
                    {'item': f'tfc:stone/{tool_type}/{rock_category}', 'nbt': {'tfc:forging_bonus': BINDING_BONUSES[binding]}}))
        
        rm.crafting_shaped(('crafting', 'stone', 'axe',     rock_category, 'multitool'), ['RM'],       {'M': f'better_stone_age:stone/multitool_head/{rock_category}', 'R': f'#forge:rods/wooden'}, utils.item_stack({'item': f'tfc:stone/axe/{rock_category}',     'nbt': {'Damage': ROCK_CATEGORY_DURABILITIES[rock_category] // 2}}))
        rm.crafting_shaped(('crafting', 'stone', 'hammer',  rock_category, 'multitool'), [' R', 'M '], {'M': f'better_stone_age:stone/multitool_head/{rock_category}', 'R': f'#forge:rods/wooden'}, utils.item_stack({'item': f'tfc:stone/hammer/{rock_category}',  'nbt': {'Damage': ROCK_CATEGORY_DURABILITIES[rock_category] // 2}}))
        rm.crafting_shaped(('crafting', 'stone', 'hoe',     rock_category, 'multitool'), ['M', 'R'],   {'M': f'better_stone_age:stone/multitool_head/{rock_category}', 'R': f'#forge:rods/wooden'}, utils.item_stack({'item': f'tfc:stone/hoe/{rock_category}',     'nbt': {'Damage': ROCK_CATEGORY_DURABILITIES[rock_category] // 2}}))
        rm.crafting_shaped(('crafting', 'stone', 'shovel',  rock_category, 'multitool'), ['R', 'M'],   {'M': f'better_stone_age:stone/multitool_head/{rock_category}', 'R': f'#forge:rods/wooden'}, utils.item_stack({'item': f'tfc:stone/shovel/{rock_category}',  'nbt': {'Damage': ROCK_CATEGORY_DURABILITIES[rock_category] // 2}}))
        rm.crafting_shaped(('crafting', 'stone', 'javelin', rock_category, 'multitool'), [' M', 'R '], {'M': f'better_stone_age:stone/multitool_head/{rock_category}', 'R': f'#forge:rods/wooden'}, utils.item_stack({'item': f'tfc:stone/javelin/{rock_category}', 'nbt': {'Damage': ROCK_CATEGORY_DURABILITIES[rock_category] // 2}}))
        
        rm.crafting_shapeless(('crafting', 'stone', 'knife', rock_category, 'multitool'), (f'better_stone_age:stone/multitool_head/{rock_category}',), utils.item_stack({'item': f'tfc:stone/knife_head/{rock_category}',   'nbt': {'Damage': ROCK_CATEGORY_DURABILITIES[rock_category] // 2}}))
    
    damage_shapeless(rm, ('crafting', 'hide_sewing', '1_plus_1'), ('tfc:small_raw_hide', 'tfc:small_raw_hide', '#forge:string', 'tfc:bone_needle'), "tfc:medium_raw_hide")
    damage_shapeless(rm, ('crafting', 'hide_sewing', '1_plus_2'), ('tfc:small_raw_hide', 'tfc:medium_raw_hide', '#forge:string', 'tfc:bone_needle'), "tfc:large_raw_hide")
    damage_shapeless(rm, ('crafting', 'hide_sewing', '2_plus_2'), ('tfc:medium_raw_hide', 'tfc:medium_raw_hide', '#forge:string', 'tfc:bone_needle'), "tfc:large_raw_hide")
    
    

def create_heating_recipes():
    print('\tCreating heating recipes...')
    for color in COLORS:
        heat_recipe(rm, ('ceramic', 'jug', f'{color}'), f'better_stone_age:ceramic/jug/unfired/{color}', POTTERY_MELT, f'better_stone_age:ceramic/jug/glazed/{color}')

def create_knapping_recipes():
    print('\tCreating knapping recipes...')
    for rock_category in ROCK_CATEGORIES:
        predicate = f'#tfc:{rock_category}_rock'
        rock_knapping(rm, ('stone', 'multitool_head', rock_category), ['  X  ', ' XXX ', ' XXX ', 'XXXXX', ' XXX '], f'better_stone_age:stone/multitool_head/{rock_category}', predicate)
def create_pot_recipes():
    print('\tCreating pot recipes...')
    for color in COLORS:
        for count in range(1, 1 + 5):
            simple_pot_recipe(rm, f'{color}_dye_from_flower_{count}', [utils.ingredient(f'#tfc:makes_{color}_dye')] * count, str(100 * count) + ' minecraft:water', str(100 * count) + f' tfc:{color}_dye', None, 2000, 730)

def create_recipes():
    print('Creating recipes...')
    create_anvil_recipes()
    create_barrel_recipes()
    create_crafting_recipes()
    create_heating_recipes()
    create_knapping_recipes()
    create_pot_recipes()
    

def create_item_models():
    print('Creating item models...')
    for color in COLORS:
        rm.item_model(('ceramic', 'jug', 'unfired', f'{color}')).with_lang(lang(f'{color} Unfired Jug'))
        contained_fluid(rm, ('ceramic', 'jug', 'glazed', f'{color}'), f'better_stone_age:item/ceramic/jug/glazed/{color}_empty', 'tfc:item/ceramic/jug_overlay').with_lang(lang(f'{color} Glazed Ceramic Jug'))
        rm.item_model(('ceramic', 'pot', 'glazed', color), f'better_stone_age:item/ceramic/pot/glazed/{color}')
    for rock_category in ROCK_CATEGORIES:
        rm.item_model(('stone', 'multitool_head', rock_category), 'better_stone_age:item/stone/multitool_head')
    
    rm.item_model(('clay_tablet'), 'better_stone_age:item/clay_tablet')
    rm.item_model(('writeable_clay_tablet'), 'better_stone_age:item/writeable_clay_tablet')
    rm.item_model(('written_clay_tablet'), 'better_stone_age:item/written_clay_tablet')
    
    rm.item_model(('sinew'), 'better_stone_age:item/sinew')
    rm.item_model(('dried_sinew'), 'better_stone_age:item/dried_sinew')
    rm.item_model(('pounded_sinew'), 'better_stone_age:item/pounded_sinew')
    rm.item_model(('sinew_string'), 'better_stone_age:item/sinew_string')
    
    
    
def create_item_heats():
    print('Creating item heat data...')
    item_heat(rm, ('ceramic', 'unfired_ceramic_jugs'), '#better_stone_age:unfired_ceramic_jugs', 0.8)


def create_entity_tags():
    print('\tCreating entity tags...')
    rm.entity_tag('drops_sinew', '#tfc:bears', 'tfc:deer', 'tfc:bongo', 'tfc:panda', 'tfc:caribou', 'tfc:gazelle', 'tfc:pig', 'tfc:cow', 'tfc:goat', 'tfc:yak', 'tfc:alpaca', 'tfc:sheep', 'tfc:musk_ox', 'tfc:horse', 'tfc:donkey', 'tfc:mule')

def create_item_tags():
    print('\tCreating item tags...')
    rm.item_tag('unfired_ceramic_jugs', 'tfc:ceramic/unfired_jug', *[f'better_stone_age:ceramic/jug/unfired/{color}' for color in COLORS])
    rm.item_tag('glazed_ceramic_jugs', 'tfc:ceramic/jug', *[f'better_stone_age:ceramic/jug/glazed/{color}' for color in COLORS])
    tfc_rm.item_tag('fluid_item_ingredient_empty_containers', '#better_stone_age:glazed_ceramic_jugs')
    tfc_rm.fluid_tag('usable_in_jug', '#tfc:dyes')
    
    rm.item_tag('bindings/weak', 'tfc:straw', 'tfc:groundcover/dead_grass', 'tfc:glue')
    rm.item_tag('bindings/medium', 'tfc:jute', 'tfc:plant/ivy', 'tfc:plant/hanging_vines', 'tfc:plant/jungle_vines')
    rm.item_tag('bindings/strong', 'tfc:jute_fiber', '#forge:string')
    
    forge_rm.item_tag('string', 'better_stone_age:sinew_string')
    
    
    for rock_category in ROCK_CATEGORIES:
        tfc_rm.item_tag(f'{rock_category}_items', f'better_stone_age:stone/multitool_head/{rock_category}')

def create_tags():
    print('Creating tags...')
    create_entity_tags()
    create_item_tags()


def read_data_from_template(rm: ResourceManager, name_parts, template: str):
    rm.write(name_parts, json.loads(template))

def create_block_models():
    print("Creating block models...")
    for color in COLORS:
        read_data_from_template(rm, ('src', 'main', 'resources', 'assets', 'better_stone_age', 'models', 'block', 'firepit_pot', color), pot_template % (color, color, color))
        
        rm.blockstate_multipart(f'ceramic/pot/{color}',
                ({'axis': 'x'}, {'model': f'better_stone_age:block/firepit_pot/{color}'}),
                ({'axis': 'z'}, {'model': f'better_stone_age:block/firepit_pot/{color}', 'y': 90}),
                ({'lit': True, 'axis': 'x'}, {'model': 'tfc:block/firepit_lit_low'}),
                ({'lit': True, 'axis': 'z'}, {'model': 'tfc:block/firepit_lit_low', 'y': 90}),
                ({'lit': False, 'axis': 'x'}, {'model': 'tfc:block/firepit_unlit'}),
                ({'lit': False, 'axis': 'z'}, {'model': 'tfc:block/firepit_unlit', 'y': 90})
            ).with_lang(lang(f'{color} Pot')).with_block_loot('tfc:powder/wood_ash', f'better_stone_age:ceramic/pot/glazed/{color}')
        rm.item_model('pot', 'tfc:item/firepit_pot')
        



def create_misc_lang():
    print('Creating misc translations...')
    rm.lang('item.minecraft.string', 'Spider Silk')
    for color in COLORS:
        rm.lang(f'item.better_stone_age.ceramic.jug.glazed.{color}.filled', '%s ' + lang(f'{color} Glazed Ceramic Jug'))
        rm.lang(f'item.better_stone_age.ceramic.pot.glazed.{color}', lang(f'{color} Pot'))
    for rock_category in ROCK_CATEGORIES:
        rm.lang(f'item.better_stone_age.stone.multitool_head.{rock_category}', lang(f'Stone Multitool Head'))
    
    rm.lang('item.better_stone_age.sinew', 'Sinew')
    rm.lang('item.better_stone_age.dried_sinew', 'Dried Sinew')
    rm.lang('item.better_stone_age.pounded_sinew', 'Pounded Sinew')
    rm.lang('item.better_stone_age.sinew_string', 'Sinew String')
    

def create_loot_tables():
    print('\tCreating loot tables...')
    tfc_rm.block_loot('tfc:calcite', {'name': 'tfc:powder/flux', 'functions': [utils.loot_functions({'function': 'minecraft:set_count', 'count': {'min': 1, 'max': 2, 'type': 'minecraft:uniform'}})]})
    tfc_rm.block_loot('tfc:charcoal_pile', {'type': 'minecraft:alternatives', 'children': [{'type': 'minecraft:item', 'name': 'tfc:powder/charcoal', 'conditions': [{'condition': 'minecraft:match_tool', 'predicate': {'tag': 'tfc:hammers'}}], 'functions': [{'function': 'minecraft:set_count', 'count': 2}]}, {'type': 'minecraft:item', 'name': 'minecraft:charcoal'}]})
    
def create_loot_modifiers():
    print('Creating loot modifiers...')
    
    loot_modifiers = []
    loot_modifier_add_itemstack_min_max(rm, loot_modifiers, 'animals_drop_sinew', '#better_stone_age:drops_sinew', 'better_stone_age:sinew', 1, 3)
    
    
    forge_rm.data(('loot_modifiers', 'global_loot_modifiers'), {'replace': False, 'entries': loot_modifiers})


def create_loot():
    print('Creating loot...')
    create_loot_tables()
    create_loot_modifiers()

def main():
    create_item_models()
    create_item_heats()
    create_tags()
    create_misc_lang()
    create_loot()
    create_recipes()
    create_block_models()
    
    forge_rm.flush()
    rm.flush()
    tfc_rm.flush()


if __name__ == '__main__':
    main()
    