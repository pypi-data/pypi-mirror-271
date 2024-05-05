import os
import re
import sys
from enum import Enum
from typing import Optional, Union

RESET: str = "\033[0m"


def is_colorization_supported() -> bool:
    """
    Checks if the current operating system supports colorization.
    :return: True if colorization is supported, False otherwise.
    :rtype: bool
    """
    file_name = 'lm_color.temp'
    # Check for Windows operating systems
    if sys.platform == 'win32':
        major, minor = sys.getwindowsversion().major, sys.getwindowsversion().minor
        return major > 10 or (major == 10 and minor >= 0)

    # Check for Linux-based operating systems
    term = os.environ.get('TERM')
    if term is None:
        return False

    if 'color' in os.popen('tput colors').read():
        return True

    try:
        with open(file_name, 'w'):
            os.system('tput setaf 1')
            os.system('tput setab 0')
            os.system('echo -n "\033[1;31m"')
            os.system('echo -n "\033[0m')

        with open(file_name, 'r') as f:
            content = f.read()
            return '\033[1;31m' in content
    finally:
        os.remove(file_name)


def is_true_color_supported() -> bool:
    """
    Verifies whether the true color format is supported by the current operating system and terminal.
    :return: True if true color format is supported, False otherwise.
    :rtype: bool
    """
    if os.name == 'nt':
        true_color_support = True
    else:
        true_color_support = os.getenv('COLORTERM') in ['truecolor', '24bit']

    return true_color_support


class Validate:
    """
    Internal utility class designed to facilitate validation across various scenarios.
    """

    @classmethod
    def validate_range(cls, values, expected_range, message) -> None:
        """
        Performs validation to ensure that the provided list of values falls within the expected range.
        If any value is outside the specified range, a ValueError is raised.
        :param values: The list of values to be validated.
        :param expected_range: The expected range (from and to) within which the values should fall.
        :param message: The message to be displayed when a ValueError is raised.
        """
        if not all(expected_range[0] <= x <= expected_range[1] for x in values):
            raise ValueError(message)

    @classmethod
    def validate_type(cls, value, expected_type, message) -> None:
        """
        Conducts validation to confirm that the provided value matches the expected type.
        If the value does not match the expected type, a ValueError is raised.
        :param value: The value to be validated.
        :param expected_type: The anticipated type for verification.
        :param message: The message to be displayed when a ValueError is raised.
        """
        if not isinstance(value, expected_type):
            raise TypeError(message)

    @classmethod
    def validate_hex(cls, hex_code: str) -> None:
        """
        Conducts validation to ensure that the provided value is in the correct HEX color format, namely #RRGGBB.
        :param hex_code: The value to be validated as a HEX color code.
        :type hex_code: str
        """
        cls.validate_type(hex_code, str, 'hex_code should be a string.')
        if not re.match(r'#[0-9a-fA-F]{6}$', hex_code.upper()):
            raise ValueError('Invalid HEX code format. Example: #RRGGBB.')

    @classmethod
    def validate_rgb(cls, *args) -> None:
        """
        Performs validation to ensure that the provided values for red (r), green (g), and blue (b)
        are in the correct format, specifically within the range of 0 to 255.
        :param args: The arguments representing red (r), green (g), and blue (b) values.
        """
        if len(args) != 3:
            raise ValueError('Exactly 3 arguments are required.')

        cls.validate_range(
            args,
            (0, 255),
            'Invalid RGB code format. RGB values should be in the range 0-255. Example: 127, 128, 255.'
        )

    @classmethod
    def validate_cmyk(cls, *args) -> None:
        """
        Performs validation to ensure that the provided values for cyan (c), magenta (m), yellow (y), and
        key (k) are in the correct format, specifically within the range of 0.0 to 1.0
        :param args: The arguments representing cyan (c), magenta (m), yellow (y), and key (k).
        """
        if len(args) != 4:
            raise ValueError('Exactly 4 arguments are required.')

        cls.validate_range(
            args,
            (0.0, 1.0),
            'Invalid CMYK code format. CMYK values should be in the range 0.0-1.0. Example: 0.7, 0.1, 1.0, 1.0.'
        )

    @classmethod
    def validate_ansi(cls, ansi: str) -> None:
        """
        Conducts validation to ensure that the provided ANSI code adheres to the expected format,
        supporting both true and standard color formats.
        :param ansi: The ANSI code to be validated.
        :type ansi: str
        """
        cls.validate_type(ansi, str, 'ansi should be a string.')

        if not re.match(r'^\033\[[0-9;]+m$', ansi) and not re.match(r'^\x1b\[[0-9;]+m$', ansi):
            raise ValueError('Invalid ANSI code format.')

        code = ansi[2:].rstrip('m')
        if not code.startswith('38;2;') and not code.startswith('48;2;') and not code.isdigit():
            raise ValueError('Unsupported ANSI code format.')


class HEXCodes:
    """
    This supporting class encapsulates constants representing HEX code formats for various colors
    sourced from Wikipedia. For licensing information, please refer to the appropriate sources.
    """
    ABSOLUTE_ZERO: str = "#0048BA"
    ACID_GREEN: str = "#B0BF1A"
    AERO: str = "#7CB9E8"
    AFRICAN_VIOLET: str = "#B284BE"
    AIR_SUPERIORITY_BLUE: str = "#72A0C1"
    ALICE_BLUE: str = "#F0F8FF"
    ALIZARIN: str = "#DB2D43"
    ALLOY_ORANGE: str = "#C46210"
    ALMOND: str = "#EED9C4"
    AMARANTH_DEEP_PURPLE: str = "#9F2B68"
    AMARANTH_PINK: str = "#F19CBB"
    AMARANTH_PURPLE: str = "#AB274F"
    AMAZON: str = "#3B7A57"
    AMBER: str = "#FFBF00"
    AMETHYST: str = "#9966CC"
    ANDROID_GREEN: str = "#3DDC84"
    ANTIQUE_BRASS: str = "#C88A65"
    ANTIQUE_BRONZE: str = "#665D1E"
    ANTIQUE_FUCHSIA: str = "#915C83"
    ANTIQUE_RUBY: str = "#841B2D"
    ANTIQUE_WHITE: str = "#FAEBD7"
    APRICOT: str = "#FBCEB1"
    AQUA: str = "#00FFFF"
    AQUAMARINE: str = "#7FFFD4"
    ARCTIC_LIME: str = "#D0FF14"
    ARTICHOKE_GREEN: str = "#4B6F44"
    ARYLIDE_YELLOW: str = "#E9D66B"
    ASH_GRAY: str = "#B2BEB5"
    ATOMIC_TANGERINE: str = "#FF9966"
    AUREOLIN: str = "#FDEE00"
    AZURE: str = "#007FFF"
    BABY_BLUE: str = "#89CFF0"
    BABY_BLUE_EYES: str = "#A1CAF1"
    BABY_PINK: str = "#F4C2C2"
    BABY_POWDER: str = "#FEFEFA"
    BAKER_MILLER_PINK: str = "#FF91AF"
    BANANA_MANIA: str = "#FAE7B5"
    BARBIE_PINK: str = "#DA1884"
    BARN_RED: str = "#7C0A02"
    BATTLESHIP_GREY: str = "#848482"
    BEAU_BLUE: str = "#BCD4E6"
    BEAVER: str = "#9F8170"
    BEIGE: str = "#F5F5DC"
    B_DAZZLED_BLUE: str = "#2E5894"
    BIG_DIP_O_RUBY: str = "#9C2542"
    BISQUE: str = "#FFE4C4"
    BISTRE: str = "#3D2B1F"
    BISTRE_BROWN: str = "#967117"
    BITTER_LEMON: str = "#CAE00D"
    BLACK_BEAN: str = "#3D0C02"
    BLACK_CORAL: str = "#54626F"
    BLACK_OLIVE: str = "#3B3C36"
    BLACK_SHADOWS: str = "#BFAFB2"
    BLANCHED_ALMOND: str = "#FFEBCD"
    BLAST_OFF_BRONZE: str = "#A57164"
    BLEU_DE_FRANCE: str = "#318CE7"
    BLIZZARD_BLUE: str = "#ACE5EE"
    BLOOD_RED: str = "#660000"
    BLUE_CRAYOLA: str = "#1F75FE"
    BLUE_MUNSELL: str = "#0093AF"
    BLUE_NCS: str = "#0087BD"
    BLUE_PANTONE: str = "#0018A8"
    BLUE_PIGMENT: str = "#333399"
    BLUE_BELL: str = "#A2A2D0"
    BLUE_GRAY_CRAYOLA: str = "#6699CC"
    BLUE_JEANS: str = "#5DADEC"
    BLUE_SAPPHIRE: str = "#126180"
    BLUE_VIOLET: str = "#8A2BE2"
    BLUE_YONDER: str = "#5072A7"
    BLUETIFUL: str = "#3C69E7"
    BLUSH: str = "#DE5D83"
    BOLE: str = "#79443B"
    BONE: str = "#E3DAC9"
    BRICK_RED: str = "#CB4154"
    BRIGHT_LILAC: str = "#D891EF"
    BRIGHT_YELLOW_CRAYOLA: str = "#FFAA1D"
    BRITISH_RACING_GREEN: str = "#004225"
    BRONZE: str = "#CD7F32"
    BROWN: str = "#964B00"
    BROWN_SUGAR: str = "#AF6E4D"
    BUD_GREEN: str = "#7BB661"
    BUFF: str = "#FFC680"
    BURGUNDY: str = "#800020"
    BURLYWOOD: str = "#DEB887"
    BURNISHED_BROWN: str = "#A17A74"
    BURNT_ORANGE: str = "#CC5500"
    BURNT_SIENNA: str = "#E97451"
    BURNT_UMBER: str = "#8A3324"
    BYZANTINE: str = "#BD33A4"
    BYZANTIUM: str = "#702963"
    CADET_BLUE: str = "#5F9EA0"
    CADET_GREY: str = "#91A3B0"
    CADMIUM_GREEN: str = "#006B3C"
    CADMIUM_ORANGE: str = "#ED872D"
    CAFE_AU_LAIT: str = "#A67B5B"
    CAFE_NOIR: str = "#4B3621"
    CAMBRIDGE_BLUE: str = "#A3C1AD"
    CAMEL: str = "#C19A6B"
    CAMEO_PINK: str = "#EFBBCC"
    CANARY: str = "#FFFF99"
    CANARY_YELLOW: str = "#FFEF00"
    CANDY_PINK: str = "#E4717A"
    CARDINAL: str = "#C41E3A"
    CARIBBEAN_GREEN: str = "#00CC99"
    CARMINE: str = "#960018"
    CARMINE_M_P: str = "#D70040"
    CARNATION_PINK: str = "#FFA6C9"
    CARNELIAN: str = "#B31B1B"
    CAROLINA_BLUE: str = "#56A0D3"
    CARROT_ORANGE: str = "#ED9121"
    CATAWBA: str = "#703642"
    CEDAR_CHEST: str = "#C95A49"
    CELADON: str = "#ACE1AF"
    CELESTE: str = "#B2FFFF"
    CERISE: str = "#DE3163"
    CERULEAN: str = "#007BA7"
    CERULEAN_BLUE: str = "#2A52BE"
    CERULEAN_FROST: str = "#6D9BC3"
    CERULEAN_CRAYOLA: str = "#1DACD6"
    CERULEAN_RGB: str = "#0040FF"
    CHAMPAGNE: str = "#F7E7CE"
    CHAMPAGNE_PINK: str = "#F1DDCF"
    CHARCOAL: str = "#36454F"
    CHARM_PINK: str = "#E68FAC"
    CHARTREUSE_WEB: str = "#80FF00"
    CHERRY_BLOSSOM_PINK: str = "#FFB7C5"
    CHESTNUT: str = "#954535"
    CHILI_RED: str = "#E23D28"
    CHINA_PINK: str = "#DE6FA1"
    CHINESE_RED: str = "#AA381E"
    CHINESE_VIOLET: str = "#856088"
    CHINESE_YELLOW: str = "#FFB200"
    CHOCOLATE_TRADITIONAL: str = "#7B3F00"
    CHOCOLATE_WEB: str = "#D2691E"
    CINEREOUS: str = "#98817B"
    CINNABAR: str = "#E34234"
    CINNAMON_SATIN: str = "#CD607E"
    CITRINE: str = "#E4D00A"
    CITRON: str = "#9FA91F"
    CLARET: str = "#7F1734"
    COFFEE: str = "#6F4E37"
    COLUMBIA_BLUE: str = "#B9D9EB"
    CONGO_PINK: str = "#F88379"
    COOL_GREY: str = "#8C92AC"
    COPPER: str = "#B87333"
    COPPER_CRAYOLA: str = "#DA8A67"
    COPPER_PENNY: str = "#AD6F69"
    COPPER_RED: str = "#CB6D51"
    COPPER_ROSE: str = "#996666"
    COQUELICOT: str = "#FF3800"
    CORAL: str = "#FF7F50"
    CORAL_PINK: str = "#F88379"
    CORDOVAN: str = "#893F45"
    CORN: str = "#FBEC5D"
    CORNFLOWER_BLUE: str = "#6495ED"
    CORNSILK: str = "#FFF8DC"
    COSMIC_COBALT: str = "#2E2D88"
    COSMIC_LATTE: str = "#FFF8E7"
    COYOTE_BROWN: str = "#81613C"
    COTTON_CANDY: str = "#FFBCD9"
    CREAM: str = "#FFFDD0"
    CRIMSON: str = "#DC143C"
    CRIMSON_UA: str = "#9E1B32"
    CULTURED_PEARL: str = "#F5F5F5"
    CYAN_PROCESS: str = "#00B7EB"
    CYBER_GRAPE: str = "#58427C"
    CYBER_YELLOW: str = "#FFD300"
    CYCLAMEN: str = "#F56FA1"
    DANDELION: str = "#FED85D"
    DARK_BROWN: str = "#654321"
    DARK_BYZANTIUM: str = "#5D3954"
    DARK_CYAN: str = "#008B8B"
    DARK_ELECTRIC_BLUE: str = "#536878"
    DARK_GOLDENROD: str = "#B8860B"
    DARK_GREEN_X11: str = "#006400"
    DARK_JUNGLE_GREEN: str = "#1A2421"
    DARK_KHAKI: str = "#BDB76B"
    DARK_LAVA: str = "#483C32"
    DARK_LIVER_HORSES: str = "#543D37"
    DARK_MAGENTA: str = "#8B008B"
    DARK_OLIVE_GREEN: str = "#556B2F"
    DARK_ORANGE: str = "#FF8C00"
    DARK_ORCHID: str = "#9932CC"
    DARK_PURPLE: str = "#301934"
    DARK_RED: str = "#8B0000"
    DARK_SALMON: str = "#E9967A"
    DARK_SEA_GREEN: str = "#8FBC8F"
    DARK_SIENNA: str = "#3C1414"
    DARK_SKY_BLUE: str = "#8CBED6"
    DARK_SLATE_BLUE: str = "#483D8B"
    DARK_SLATE_GRAY: str = "#2F4F4F"
    DARK_SPRING_GREEN: str = "#177245"
    DARK_TURQUOISE: str = "#00CED1"
    DARK_VIOLET: str = "#9400D3"
    DAVY_S_GREY: str = "#555555"
    DEEP_CERISE: str = "#DA3287"
    DEEP_CHAMPAGNE: str = "#FAD6A5"
    DEEP_CHESTNUT: str = "#B94E48"
    DEEP_JUNGLE_GREEN: str = "#004B49"
    DEEP_PINK: str = "#FF1493"
    DEEP_SAFFRON: str = "#FF9933"
    DEEP_SKY_BLUE: str = "#00BFFF"
    DEEP_SPACE_SPARKLE: str = "#4A646C"
    DEEP_TAUPE: str = "#7E5E60"
    DENIM: str = "#1560BD"
    DENIM_BLUE: str = "#2243B6"
    DESERT: str = "#C19A6B"
    DESERT_SAND: str = "#EDC9AF"
    DIM_GRAY: str = "#696969"
    DODGER_BLUE: str = "#1E90FF"
    DRAB_DARK_BROWN: str = "#4A412A"
    DUKE_BLUE: str = "#00009C"
    DUTCH_WHITE: str = "#EFDFBB"
    EBONY: str = "#555D50"
    ECRU: str = "#C2B280"
    EERIE_BLACK: str = "#1B1B1B"
    EGGPLANT: str = "#614051"
    EGGSHELL: str = "#F0EAD6"
    ELECTRIC_LIME: str = "#CCFF00"
    ELECTRIC_PURPLE: str = "#BF00FF"
    ELECTRIC_VIOLET: str = "#8F00FF"
    EMERALD: str = "#50C878"
    EMINENCE: str = "#6C3082"
    ENGLISH_LAVENDER: str = "#B48395"
    ENGLISH_RED: str = "#AB4B52"
    ENGLISH_VERMILLION: str = "#CC474B"
    ENGLISH_VIOLET: str = "#563C5C"
    ERIN: str = "#00FF40"
    ETON_BLUE: str = "#96C8A2"
    FALLOW: str = "#C19A6B"
    FALU_RED: str = "#801818"
    FANDANGO: str = "#B53389"
    FANDANGO_PINK: str = "#DE5285"
    FAWN: str = "#E5AA70"
    FERN_GREEN: str = "#4F7942"
    FIELD_DRAB: str = "#6C541E"
    FIERY_ROSE: str = "#FF5470"
    FINN: str = "#683068"
    FIREBRICK: str = "#B22222"
    FIRE_ENGINE_RED: str = "#CE2029"
    FLAME: str = "#E25822"
    FLAX: str = "#EEDC82"
    FLIRT: str = "#A2006D"
    FLORAL_WHITE: str = "#FFFAF0"
    FOREST_GREEN_WEB: str = "#228B22"
    FRENCH_BEIGE: str = "#A67B5B"
    FRENCH_BISTRE: str = "#856D4D"
    FRENCH_BLUE: str = "#0072BB"
    FRENCH_FUCHSIA: str = "#FD3F92"
    FRENCH_LILAC: str = "#86608E"
    FRENCH_LIME: str = "#9EFD38"
    FRENCH_MAUVE: str = "#D473D4"
    FRENCH_PINK: str = "#FD6C9E"
    FRENCH_RASPBERRY: str = "#C72C48"
    FRENCH_SKY_BLUE: str = "#77B5FE"
    FRENCH_VIOLET: str = "#8806CE"
    FROSTBITE: str = "#E936A7"
    FUCHSIA: str = "#FF00FF"
    FUCHSIA_CRAYOLA: str = "#C154C1"
    FULVOUS: str = "#E48400"
    FUZZY_WUZZY: str = "#87421F"
    GAINSBORO: str = "#DCDCDC"
    GAMBOGE: str = "#E49B0F"
    GENERIC_VIRIDIAN: str = "#007F66"
    GHOST_WHITE: str = "#F8F8FF"
    GLAUCOUS: str = "#6082B6"
    GLOSSY_GRAPE: str = "#AB92B3"
    GO_GREEN: str = "#00AB66"
    GOLD_METALLIC: str = "#D4AF37"
    GOLD_WEB_GOLDEN: str = "#FFD700"
    GOLD_CRAYOLA: str = "#E6BE8A"
    GOLD_FUSION: str = "#85754E"
    GOLDEN_BROWN: str = "#996515"
    GOLDEN_POPPY: str = "#FCC200"
    GOLDEN_YELLOW: str = "#FFDF00"
    GOLDENROD: str = "#DAA520"
    GOTHAM_GREEN: str = "#00573F"
    GRANITE_GRAY: str = "#676767"
    GRANNY_SMITH_APPLE: str = "#A8E4A0"
    GRAY_WEB: str = "#808080"
    GRAY_X11_GRAY: str = "#BEBEBE"
    GREEN_CRAYOLA: str = "#1CAC78"
    GREEN_WEB: str = "#008000"
    GREEN_MUNSELL: str = "#00A877"
    GREEN_NCS: str = "#009F6B"
    GREEN_PANTONE: str = "#00AD43"
    GREEN_PIGMENT: str = "#00A550"
    GREEN_BLUE: str = "#1164B4"
    GREEN_LIZARD: str = "#A7F432"
    GREEN_SHEEN: str = "#6EAEA1"
    GUNMETAL: str = "#2a3439"
    HANSA_YELLOW: str = "#E9D66B"
    HARLEQUIN: str = "#3FFF00"
    HARVEST_GOLD: str = "#DA9100"
    HEAT_WAVE: str = "#FF7A00"
    HELIOTROPE: str = "#DF73FF"
    HELIOTROPE_GRAY: str = "#AA98A9"
    HOLLYWOOD_CERISE: str = "#F400A1"
    HONOLULU_BLUE: str = "#006DB0"
    HOOKER_S_GREEN: str = "#49796B"
    HOT_MAGENTA: str = "#FF1DCE"
    HOT_PINK: str = "#FF69B4"
    HUNTER_GREEN: str = "#355E3B"
    ICEBERG: str = "#71A6D2"
    ILLUMINATING_EMERALD: str = "#319177"
    IMPERIAL_RED: str = "#ED2939"
    INCHWORM: str = "#B2EC5D"
    INDEPENDENCE: str = "#4C516D"
    INDIA_GREEN: str = "#138808"
    INDIAN_RED: str = "#CD5C5C"
    INDIAN_YELLOW: str = "#E3A857"
    INDIGO: str = "#6A5DFF"
    INDIGO_DYE: str = "#00416A"
    INTERNATIONAL_KLEIN_BLUE: str = "#130a8f"
    INTERNATIONAL_ORANGE_ENGINEERING: str = "#BA160C"
    INTERNATIONAL_ORANGE_GOLDEN_GATE_BRIDGE: str = "#C0362C"
    IRRESISTIBLE: str = "#B3446C"
    ISABELLINE: str = "#F4F0EC"
    ITALIAN_SKY_BLUE: str = "#B2FFFF"
    IVORY: str = "#FFFFF0"
    JAPANESE_CARMINE: str = "#9D2933"
    JAPANESE_VIOLET: str = "#5B3256"
    JASMINE: str = "#F8DE7E"
    JAZZBERRY_JAM: str = "#A50B5E"
    JET: str = "#343434"
    JONQUIL: str = "#F4CA16"
    JUNE_BUD: str = "#BDDA57"
    JUNGLE_GREEN: str = "#29AB87"
    KELLY_GREEN: str = "#4CBB17"
    KEPPEL: str = "#3AB09E"
    KEY_LIME: str = "#E8F48C"
    KHAKI_WEB: str = "#C3B091"
    KHAKI_X11_LIGHT_KHAKI: str = "#F0E68C"
    KOBE: str = "#882D17"
    KOBI: str = "#E79FC4"
    KOBICHA: str = "#6B4423"
    KSU_PURPLE: str = "#512888"
    LANGUID_LAVENDER: str = "#D6CADD"
    LAPIS_LAZULI: str = "#26619C"
    LASER_LEMON: str = "#FFFF66"
    LAUREL_GREEN: str = "#A9BA9D"
    LAVA: str = "#CF1020"
    LAVENDER_FLORAL: str = "#B57EDC"
    LAVENDER_WEB: str = "#E6E6FA"
    LAVENDER_BLUE: str = "#CCCCFF"
    LAVENDER_BLUSH: str = "#FFF0F5"
    LAVENDER_GRAY: str = "#C4C3D0"
    LAWN_GREEN: str = "#7CFC00"
    LEMON: str = "#FFF700"
    LEMON_CHIFFON: str = "#FFFACD"
    LEMON_CURRY: str = "#CCA01D"
    LEMON_GLACIER: str = "#FDFF00"
    LEMON_MERINGUE: str = "#F6EABE"
    LEMON_YELLOW: str = "#FFF44F"
    LEMON_YELLOW_CRAYOLA: str = "#FFFF9F"
    LIBERTY: str = "#545AA7"
    LIGHT_BLUE: str = "#ADD8E6"
    LIGHT_CORAL: str = "#F08080"
    LIGHT_CORNFLOWER_BLUE: str = "#93CCEA"
    LIGHT_CYAN: str = "#E0FFFF"
    LIGHT_FRENCH_BEIGE: str = "#C8AD7F"
    LIGHT_GOLDENROD_YELLOW: str = "#FAFAD2"
    LIGHT_GRAY: str = "#D3D3D3"
    LIGHT_GREEN: str = "#90EE90"
    LIGHT_ORANGE: str = "#FED8B1"
    LIGHT_PERIWINKLE: str = "#C5CBE1"
    LIGHT_PINK: str = "#FFB6C1"
    LIGHT_SALMON: str = "#FFA07A"
    LIGHT_SEA_GREEN: str = "#20B2AA"
    LIGHT_SKY_BLUE: str = "#87CEFA"
    LIGHT_SLATE_GRAY: str = "#778899"
    LIGHT_STEEL_BLUE: str = "#B0C4DE"
    LIGHT_YELLOW: str = "#FFFFE0"
    LILAC: str = "#C8A2C8"
    LILAC_LUSTER: str = "#AE98AA"
    LIME_COLOR_WHEEL: str = "#BFFF00"
    LIME_WEB_X11_GREEN: str = "#00FF00"
    LIME_GREEN: str = "#32CD32"
    LINCOLN_GREEN: str = "#195905"
    LINEN: str = "#FAF0E6"
    LION: str = "#DECC9C"
    LISERAN_PURPLE: str = "#DE6FA1"
    LITTLE_BOY_BLUE: str = "#6CA0DC"
    LIVER: str = "#674C47"
    LIVER_DOGS: str = "#B86D29"
    LIVER_ORGAN: str = "#6C2E1F"
    LIVER_CHESTNUT: str = "#987456"
    LIVID: str = "#6699CC"
    MACARONI_AND_CHEESE: str = "#FFBD88"
    MADDER_LAKE: str = "#CC3336"
    MAGENTA_CRAYOLA: str = "#F653A6"
    MAGENTA_DYE: str = "#CA1F7B"
    MAGENTA_PANTONE: str = "#D0417E"
    MAGENTA_PROCESS: str = "#FF0090"
    MAGENTA_HAZE: str = "#9F4576"
    MAGIC_MINT: str = "#AAF0D1"
    MAGNOLIA: str = "#F2E8D7"
    MAHOGANY: str = "#C04000"
    MAIZE: str = "#FBEC5D"
    MAIZE_CRAYOLA: str = "#F2C649"
    MAJORELLE_BLUE: str = "#6050DC"
    MALACHITE: str = "#0BDA51"
    MANATEE: str = "#979AAA"
    MANDARIN: str = "#F37A48"
    MANGO: str = "#FDBE02"
    MANGO_TANGO: str = "#FF8243"
    MANTIS: str = "#74C365"
    MARDI_GRAS: str = "#880085"
    MARIGOLD: str = "#EAA221"
    MAROON_CRAYOLA: str = "#C32148"
    MAROON_WEB: str = "#800000"
    MAROON_X11: str = "#B03060"
    MAUVE: str = "#E0B0FF"
    MAUVE_TAUPE: str = "#915F6D"
    MAUVELOUS: str = "#EF98AA"
    MAXIMUM_BLUE: str = "#47ABCC"
    MAXIMUM_BLUE_GREEN: str = "#30BFBF"
    MAXIMUM_BLUE_PURPLE: str = "#ACACE6"
    MAXIMUM_GREEN: str = "#5E8C31"
    MAXIMUM_GREEN_YELLOW: str = "#D9E650"
    MAXIMUM_PURPLE: str = "#733380"
    MAXIMUM_RED: str = "#D92121"
    MAXIMUM_RED_PURPLE: str = "#A63A79"
    MAXIMUM_YELLOW: str = "#FAFA37"
    MAXIMUM_YELLOW_RED: str = "#F2BA49"
    MAY_GREEN: str = "#4C9141"
    MAYA_BLUE: str = "#73C2FB"
    MEDIUM_AQUAMARINE: str = "#66DDAA"
    MEDIUM_BLUE: str = "#0000CD"
    MEDIUM_CANDY_APPLE_RED: str = "#E2062C"
    MEDIUM_CARMINE: str = "#AF4035"
    MEDIUM_CHAMPAGNE: str = "#F3E5AB"
    MEDIUM_ORCHID: str = "#BA55D3"
    MEDIUM_PURPLE: str = "#9370DB"
    MEDIUM_SEA_GREEN: str = "#3CB371"
    MEDIUM_SLATE_BLUE: str = "#7B68EE"
    MEDIUM_SPRING_GREEN: str = "#00FA9A"
    MEDIUM_TURQUOISE: str = "#48D1CC"
    MEDIUM_VIOLET_RED: str = "#C71585"
    MELLOW_APRICOT: str = "#F8B878"
    MELLOW_YELLOW: str = "#F8DE7E"
    MELON: str = "#FEBAAD"
    METALLIC_GOLD: str = "#D3AF37"
    METALLIC_SEAWEED: str = "#0A7E8C"
    METALLIC_SUNBURST: str = "#9C7C38"
    MEXICAN_PINK: str = "#E4007C"
    MIDDLE_BLUE: str = "#7ED4E6"
    MIDDLE_BLUE_GREEN: str = "#8DD9CC"
    MIDDLE_BLUE_PURPLE: str = "#8B72BE"
    MIDDLE_GREY: str = "#8B8680"
    MIDDLE_GREEN: str = "#4D8C57"
    MIDDLE_GREEN_YELLOW: str = "#ACBF60"
    MIDDLE_PURPLE: str = "#D982B5"
    MIDDLE_RED: str = "#E58E73"
    MIDDLE_RED_PURPLE: str = "#A55353"
    MIDDLE_YELLOW: str = "#FFEB00"
    MIDDLE_YELLOW_RED: str = "#ECB176"
    MIDNIGHT: str = "#702670"
    MIDNIGHT_BLUE: str = "#191970"
    MIDNIGHT_GREEN_EAGLE_GREEN: str = "#004953"
    MIKADO_YELLOW: str = "#FFC40C"
    MIMI_PINK: str = "#FFDAE9"
    MINDARO: str = "#E3F988"
    MING: str = "#36747D"
    MINION_YELLOW: str = "#F5E050"
    MINT: str = "#3EB489"
    MINT_CREAM: str = "#F5FFFA"
    MINT_GREEN: str = "#98FF98"
    MISTY_MOSS: str = "#BBB477"
    MISTY_ROSE: str = "#FFE4E1"
    MODE_BEIGE: str = "#967117"
    MONA_LISA: str = "#FF948E"
    MORNING_BLUE: str = "#8DA399"
    MOSS_GREEN: str = "#8A9A5B"
    MOUNTAIN_MEADOW: str = "#30BA8F"
    MOUNTBATTEN_PINK: str = "#997A8D"
    MSU_GREEN: str = "#18453B"
    MULBERRY: str = "#C54B8C"
    MULBERRY_CRAYOLA: str = "#C8509B"
    MUSTARD: str = "#FFDB58"
    MYRTLE_GREEN: str = "#317873"
    MYSTIC: str = "#D65282"
    MYSTIC_MAROON: str = "#AD4379"
    NADESHIKO_PINK: str = "#F6ADC6"
    NAPLES_YELLOW: str = "#FADA5E"
    NAVAJO_WHITE: str = "#FFDEAD"
    NAVY_BLUE: str = "#000080"
    NAVY_BLUE_CRAYOLA: str = "#1974D2"
    NEON_BLUE: str = "#4666FF"
    NEON_GREEN: str = "#39FF14"
    NEON_FUCHSIA: str = "#FE4164"
    NEW_CAR: str = "#214FC6"
    NEW_YORK_PINK: str = "#D7837F"
    NICKEL: str = "#727472"
    NON_PHOTO_BLUE: str = "#A4DDED"
    NYANZA: str = "#E9FFDB"
    OCHRE: str = "#CC7722"
    OLD_BURGUNDY: str = "#43302E"
    OLD_GOLD: str = "#CFB53B"
    OLD_LACE: str = "#FDF5E6"
    OLD_LAVENDER: str = "#796878"
    OLD_MAUVE: str = "#673147"
    OLD_ROSE: str = "#C08081"
    OLD_SILVER: str = "#848482"
    OLIVE: str = "#808000"
    OLIVE_DRAB_3: str = "#6B8E23"
    OLIVE_DRAB_7: str = "#3C341F"
    OLIVE_GREEN: str = "#B5B35C"
    OLIVINE: str = "#9AB973"
    ONYX: str = "#353839"
    OPAL: str = "#A8C3BC"
    OPERA_MAUVE: str = "#B784A7"
    ORANGE: str = "#FF7F00"
    ORANGE_CRAYOLA: str = "#FF7538"
    ORANGE_PANTONE: str = "#FF5800"
    ORANGE_WEB: str = "#FFA500"
    ORANGE_PEEL: str = "#FF9F00"
    ORANGE_RED: str = "#FF681F"
    ORANGE_RED_CRAYOLA: str = "#FF5349"
    ORANGE_SODA: str = "#FA5B3D"
    ORANGE_YELLOW: str = "#F5BD1F"
    ORANGE_YELLOW_CRAYOLA: str = "#F8D568"
    ORCHID: str = "#DA70D6"
    ORCHID_PINK: str = "#F2BDCD"
    ORCHID_CRAYOLA: str = "#E29CD2"
    OUTER_SPACE_CRAYOLA: str = "#2D383A"
    OUTRAGEOUS_ORANGE: str = "#FF6E4A"
    OXBLOOD: str = "#4A0000"
    OXFORD_BLUE: str = "#002147"
    OU_CRIMSON_RED: str = "#841617"
    PACIFIC_BLUE: str = "#1CA9C9"
    PAKISTAN_GREEN: str = "#006600"
    PALATINATE_PURPLE: str = "#682860"
    PALE_AQUA: str = "#BED3E5"
    PALE_CERULEAN: str = "#9BC4E2"
    PALE_DOGWOOD: str = "#ED7A9B"
    PALE_PINK: str = "#FADADD"
    PALE_PURPLE_PANTONE: str = "#FAE6FA"
    PALE_SPRING_BUD: str = "#ECEBBD"
    PANSY_PURPLE: str = "#78184A"
    PAOLO_VERONESE_GREEN: str = "#009B7D"
    PAPAYA_WHIP: str = "#FFEFD5"
    PARADISE_PINK: str = "#E63E62"
    PARCHMENT: str = "#F1E9D2"
    PARIS_GREEN: str = "#50C878"
    PASTEL_PINK: str = "#DEA5A4"
    PATRIARCH: str = "#800080"
    PAUA: str = "#1F005E"
    PAYNE_S_GREY: str = "#536878"
    PEACH: str = "#FFE5B4"
    PEACH_CRAYOLA: str = "#FFCBA4"
    PEACH_PUFF: str = "#FFDAB9"
    PEAR: str = "#D1E231"
    PEARLY_PURPLE: str = "#B768A2"
    PERIWINKLE: str = "#CCCCFF"
    PERIWINKLE_CRAYOLA: str = "#C3CDE6"
    PERMANENT_GERANIUM_LAKE: str = "#E12C2C"
    PERSIAN_BLUE: str = "#1C39BB"
    PERSIAN_GREEN: str = "#00A693"
    PERSIAN_INDIGO: str = "#32127A"
    PERSIAN_ORANGE: str = "#D99058"
    PERSIAN_PINK: str = "#F77FBE"
    PERSIAN_PLUM: str = "#701C1C"
    PERSIAN_RED: str = "#CC3333"
    PERSIAN_ROSE: str = "#FE28A2"
    PERSIMMON: str = "#EC5800"
    PEWTER_BLUE: str = "#8BA8B7"
    PHLOX: str = "#DF00FF"
    PHTHALO_BLUE: str = "#000F89"
    PHTHALO_GREEN: str = "#123524"
    PICOTEE_BLUE: str = "#2E2787"
    PICTORIAL_CARMINE: str = "#C30B4E"
    PIGGY_PINK: str = "#FDDDE6"
    PINE_GREEN: str = "#01796F"
    PINK: str = "#FFC0CB"
    PINK_PANTONE: str = "#D74894"
    PINK_LACE: str = "#FFDDF4"
    PINK_LAVENDER: str = "#D8B2D1"
    PINK_SHERBET: str = "#F78FA7"
    PISTACHIO: str = "#93C572"
    PLATINUM: str = "#E5E4E2"
    PLUM: str = "#8E4585"
    PLUM_WEB: str = "#DDA0DD"
    PLUMP_PURPLE: str = "#5946B2"
    POLISHED_PINE: str = "#5DA493"
    POMP_AND_POWER: str = "#86608E"
    POPSTAR: str = "#BE4F62"
    PORTLAND_ORANGE: str = "#FF5A36"
    POWDER_BLUE: str = "#B0E0E6"
    PRAIRIE_GOLD: str = "#E1CA7A"
    PRINCETON_ORANGE: str = "#F58025"
    PRUNE: str = "#701C1C"
    PRUSSIAN_BLUE: str = "#003153"
    PSYCHEDELIC_PURPLE: str = "#DF00FF"
    PUCE: str = "#CC8899"
    PULLMAN_BROWN_UPS_BROWN: str = "#644117"
    PUMPKIN: str = "#FF7518"
    PURPLE: str = "#6A0DAD"
    PURPLE_WEB: str = "#800080"
    PURPLE_MUNSELL: str = "#9F00C5"
    PURPLE_X11: str = "#A020F0"
    PURPLE_MOUNTAIN_MAJESTY: str = "#9678B6"
    PURPLE_NAVY: str = "#4E5180"
    PURPLE_PIZZAZZ: str = "#FE4EDA"
    PURPLE_PLUM: str = "#9C51B6"
    PURPUREUS: str = "#9A4EAE"
    QUEEN_BLUE: str = "#436B95"
    QUEEN_PINK: str = "#E8CCD7"
    QUICK_SILVER: str = "#A6A6A6"
    QUINACRIDONE_MAGENTA: str = "#8E3A59"
    RADICAL_RED: str = "#FF355E"
    RAISIN_BLACK: str = "#242124"
    RAJAH: str = "#FBAB60"
    RASPBERRY: str = "#E30B5D"
    RASPBERRY_GLACE: str = "#915F6D"
    RASPBERRY_ROSE: str = "#B3446C"
    RAW_SIENNA: str = "#D68A59"
    RAW_UMBER: str = "#826644"
    RAZZLE_DAZZLE_ROSE: str = "#FF33CC"
    RAZZMATAZZ: str = "#E3256B"
    RAZZMIC_BERRY: str = "#8D4E85"
    REBECCA_PURPLE: str = "#663399"
    RED_CRAYOLA: str = "#EE204D"
    RED_MUNSELL: str = "#F2003C"
    RED_NCS: str = "#C40233"
    RED_PANTONE: str = "#ED2939"
    RED_PIGMENT: str = "#ED1C24"
    RED_RYB: str = "#FE2712"
    RED_ORANGE: str = "#FF5349"
    RED_ORANGE_CRAYOLA: str = "#FF681F"
    RED_ORANGE_COLOR_WHEEL: str = "#FF4500"
    RED_PURPLE: str = "#E40078"
    RED_SALSA: str = "#FD3A4A"
    RED_VIOLET: str = "#C71585"
    RED_VIOLET_CRAYOLA: str = "#C0448F"
    RED_VIOLET_COLOR_WHEEL: str = "#922B3E"
    REDWOOD: str = "#A45A52"
    RESOLUTION_BLUE: str = "#002387"
    RHYTHM: str = "#777696"
    RICH_BLACK: str = "#004040"
    RICH_BLACK_FOGRA29: str = "#010B13"
    RICH_BLACK_FOGRA39: str = "#010203"
    RIFLE_GREEN: str = "#444C38"
    ROBIN_EGG_BLUE: str = "#00CCCC"
    ROCKET_METALLIC: str = "#8A7F80"
    ROJO_SPANISH_RED: str = "#A91101"
    ROMAN_SILVER: str = "#838996"
    ROSE: str = "#FF007F"
    ROSE_BONBON: str = "#F9429E"
    ROSE_DUST: str = "#9E5E6F"
    ROSE_EBONY: str = "#674846"
    ROSE_MADDER: str = "#E32636"
    ROSE_PINK: str = "#FF66CC"
    ROSE_POMPADOUR: str = "#ED7A9B"
    ROSE_RED: str = "#C21E56"
    ROSE_TAUPE: str = "#905D5D"
    ROSE_VALE: str = "#AB4E52"
    ROSEWOOD: str = "#65000B"
    ROSSO_CORSA: str = "#D40000"
    ROSY_BROWN: str = "#BC8F8F"
    ROYAL_BLUE_DARK: str = "#002366"
    ROYAL_BLUE_LIGHT: str = "#4169E1"
    ROYAL_PURPLE: str = "#7851A9"
    ROYAL_YELLOW: str = "#FADA5E"
    RUBER: str = "#CE4676"
    RUBINE_RED: str = "#D10056"
    RUBY: str = "#E0115F"
    RUBY_RED: str = "#9B111E"
    RUFOUS: str = "#A81C07"
    RUSSET: str = "#80461B"
    RUSSIAN_GREEN: str = "#679267"
    RUSSIAN_VIOLET: str = "#32174D"
    RUST: str = "#B7410E"
    RUSTY_RED: str = "#DA2C43"
    SACRAMENTO_STATE_GREEN: str = "#043927"
    SADDLE_BROWN: str = "#8B4513"
    SAFETY_ORANGE: str = "#FF7800"
    SAFETY_ORANGE_BLAZE_ORANGE: str = "#FF6700"
    SAFETY_YELLOW: str = "#EED202"
    SAFFRON: str = "#F4C430"
    SAGE: str = "#BCB88A"
    ST_PATRICK_S_BLUE: str = "#23297A"
    SALMON: str = "#FA8072"
    SALMON_PINK: str = "#FF91A4"
    SAND: str = "#C2B280"
    SAND_DUNE: str = "#967117"
    SANDY_BROWN: str = "#F4A460"
    SAP_GREEN: str = "#507D2A"
    SAPPHIRE: str = "#0F52BA"
    SAPPHIRE_BLUE: str = "#0067A5"
    SAPPHIRE_CRAYOLA: str = "#2D5DA1"
    SATIN_SHEEN_GOLD: str = "#CBA135"
    SCARLET: str = "#FF2400"
    SCHAUSS_PINK: str = "#FF91AF"
    SCHOOL_BUS_YELLOW: str = "#FFD800"
    SCREAMIN_GREEN: str = "#66FF66"
    SEA_GREEN: str = "#2E8B57"
    SEA_GREEN_CRAYOLA: str = "#00FFCD"
    SEANCE: str = "#612086"
    SEAL_BROWN: str = "#59260B"
    SEASHELL: str = "#FFF5EE"
    SECRET: str = "#764374"
    SELECTIVE_YELLOW: str = "#FFBA00"
    SEPIA: str = "#704214"
    SHADOW: str = "#8A795D"
    SHADOW_BLUE: str = "#778BA5"
    SHAMROCK_GREEN: str = "#009E60"
    SHEEN_GREEN: str = "#8FD400"
    SHIMMERING_BLUSH: str = "#D98695"
    SHINY_SHAMROCK: str = "#5FA778"
    SHOCKING_PINK: str = "#FC0FC0"
    SHOCKING_PINK_CRAYOLA: str = "#FF6FFF"
    SIENNA: str = "#882D17"
    SILVER: str = "#C0C0C0"
    SILVER_CRAYOLA: str = "#C9C0BB"
    SILVER_METALLIC: str = "#AAA9AD"
    SILVER_CHALICE: str = "#ACACAC"
    SILVER_PINK: str = "#C4AEAD"
    SILVER_SAND: str = "#BFC1C2"
    SINOPIA: str = "#CB410B"
    SIZZLING_RED: str = "#FF3855"
    SIZZLING_SUNRISE: str = "#FFDB00"
    SKOBELOFF: str = "#007474"
    SKY_BLUE: str = "#87CEEB"
    SKY_BLUE_CRAYOLA: str = "#76D7EA"
    SKY_MAGENTA: str = "#CF71AF"
    SLATE_BLUE: str = "#6A5ACD"
    SLATE_GRAY: str = "#708090"
    SLIMY_GREEN: str = "#299617"
    SMITTEN: str = "#C84186"
    SMOKY_BLACK: str = "#100C08"
    SNOW: str = "#FFFAFA"
    SOLID_PINK: str = "#893843"
    SONIC_SILVER: str = "#757575"
    SPACE_CADET: str = "#1D2951"
    SPANISH_BISTRE: str = "#807532"
    SPANISH_BLUE: str = "#0070B8"
    SPANISH_CARMINE: str = "#D10047"
    SPANISH_GRAY: str = "#989898"
    SPANISH_GREEN: str = "#009150"
    SPANISH_ORANGE: str = "#E86100"
    SPANISH_PINK: str = "#F7BFBE"
    SPANISH_RED: str = "#E60026"
    SPANISH_SKY_BLUE: str = "#00FFFE"
    SPANISH_VIOLET: str = "#4C2882"
    SPANISH_VIRIDIAN: str = "#007F5C"
    SPRING_BUD: str = "#A7FC00"
    SPRING_FROST: str = "#87FF2A"
    SPRING_GREEN: str = "#00FF7F"
    SPRING_GREEN_CRAYOLA: str = "#ECEBBD"
    STAR_COMMAND_BLUE: str = "#007BB8"
    STEEL_BLUE: str = "#4682B4"
    STEEL_PINK: str = "#CC33CC"
    STIL_DE_GRAIN_YELLOW: str = "#FADA5E"
    STIZZA: str = "#900910"
    STRAW: str = "#E4D96F"
    STRAWBERRY: str = "#FA5053"
    STRAWBERRY_BLONDE: str = "#FF9361"
    STRONG_LIME_GREEN: str = "#33CC33"
    SUGAR_PLUM: str = "#914E75"
    SUNGLOW: str = "#FFCC33"
    SUNRAY: str = "#E3AB57"
    SUNSET: str = "#FAD6A5"
    SUPER_PINK: str = "#CF6BA9"
    SWEET_BROWN: str = "#A83731"
    SYRACUSE_ORANGE: str = "#D44500"
    TAN: str = "#D2B48C"
    TAN_CRAYOLA: str = "#D99A6C"
    TANGERINE: str = "#F28500"
    TANGO_PINK: str = "#E4717A"
    TART_ORANGE: str = "#FB4D46"
    TAUPE: str = "#483C32"
    TAUPE_GRAY: str = "#8B8589"
    TEA_GREEN: str = "#D0F0C0"
    TEA_ROSE: str = "#F4C2C2"
    TEAL: str = "#008080"
    TEAL_BLUE: str = "#367588"
    TECHNOBOTANICA: str = "#00FFBF"
    TELEMAGENTA: str = "#CF3476"
    TENNE_TAWNY: str = "#CD5700"
    TERRA_COTTA: str = "#E2725B"
    THISTLE: str = "#D8BFD8"
    THULIAN_PINK: str = "#DE6FA1"
    TICKLE_ME_PINK: str = "#FC89AC"
    TIFFANY_BLUE: str = "#0ABAB5"
    TIMBERWOLF: str = "#DBD7D2"
    TITANIUM_YELLOW: str = "#EEE600"
    TOMATO: str = "#FF6347"
    TOURMALINE: str = "#86A1A9"
    TROPICAL_RAINFOREST: str = "#00755E"
    TRUE_BLUE: str = "#2D68C4"
    TRYPAN_BLUE: str = "#1C05B3"
    TUFTS_BLUE: str = "#3E8EDE"
    TUMBLEWEED: str = "#DEAA88"
    TURQUOISE: str = "#40E0D0"
    TURQUOISE_BLUE: str = "#00FFEF"
    TURQUOISE_GREEN: str = "#A0D6B4"
    TURTLE_GREEN: str = "#8A9A5B"
    TUSCAN: str = "#FAD6A5"
    TUSCAN_BROWN: str = "#6F4E37"
    TUSCAN_RED: str = "#7C4848"
    TUSCAN_TAN: str = "#A67B5B"
    TUSCANY: str = "#C09999"
    TWILIGHT_LAVENDER: str = "#8A496B"
    TYRIAN_PURPLE: str = "#66023C"
    UA_BLUE: str = "#0033AA"
    UA_RED: str = "#D9004C"
    ULTRAMARINE: str = "#3F00FF"
    ULTRAMARINE_BLUE: str = "#4166F5"
    ULTRA_PINK: str = "#FF6FFF"
    ULTRA_RED: str = "#FC6C85"
    UMBER: str = "#635147"
    UNBLEACHED_SILK: str = "#FFDDCA"
    UNITED_NATIONS_BLUE: str = "#009EDB"
    UNIVERSITY_OF_PENNSYLVANIA_RED: str = "#A50021"
    UNMELLOW_YELLOW: str = "#FFFF66"
    UP_FOREST_GREEN: str = "#014421"
    UP_MAROON: str = "#7B1113"
    UPSDELL_RED: str = "#AE2029"
    URANIAN_BLUE: str = "#AFDBF5"
    USAFA_BLUE: str = "#004F98"
    VAN_DYKE_BROWN: str = "#664228"
    VANILLA: str = "#F3E5AB"
    VANILLA_ICE: str = "#F38FA9"
    VEGAS_GOLD: str = "#C5B358"
    VENETIAN_RED: str = "#C80815"
    VERDIGRIS: str = "#43B3AE"
    VERMILION: str = "#E34234"
    VERONICA: str = "#A020F0"
    VIOLET: str = "#8F00FF"
    VIOLET_COLOR_WHEEL: str = "#7F00FF"
    VIOLET_CRAYOLA: str = "#963D7F"
    VIOLET_RYB: str = "#8601AF"
    VIOLET_WEB: str = "#EE82EE"
    VIOLET_BLUE: str = "#324AB2"
    VIOLET_BLUE_CRAYOLA: str = "#766EC8"
    VIOLET_RED: str = "#F75394"
    VIOLET_REDPERBANG: str = "#F0599C"
    VIRIDIAN: str = "#40826D"
    VIRIDIAN_GREEN: str = "#009698"
    VIVID_BURGUNDY: str = "#9F1D35"
    VIVID_SKY_BLUE: str = "#00CCFF"
    VIVID_TANGERINE: str = "#FFA089"
    VIVID_VIOLET: str = "#9F00FF"
    VOLT: str = "#CEFF00"
    WARM_BLACK: str = "#004242"
    WEEZY_BLUE: str = "#189BCC"
    WHEAT: str = "#F5DEB3"
    WILD_BLUE_YONDER: str = "#A2ADD0"
    WILD_ORCHID: str = "#D470A2"
    WILD_STRAWBERRY: str = "#FF43A4"
    WILD_WATERMELON: str = "#FC6C85"
    WINDSOR_TAN: str = "#A75502"
    WINE: str = "#722F37"
    WINE_DREGS: str = "#673147"
    WINTER_SKY: str = "#FF007C"
    WINTERGREEN_DREAM: str = "#56887D"
    WISTERIA: str = "#C9A0DC"
    WOOD_BROWN: str = "#C19A6B"
    XANADU: str = "#738678"
    XANTHIC: str = "#EEED09"
    XANTHOUS: str = "#F1B42F"
    YALE_BLUE: str = "#00356B"
    YELLOW_CRAYOLA: str = "#FCE883"
    YELLOW_MUNSELL: str = "#EFCC00"
    YELLOW_NCS: str = "#FFD300"
    YELLOW_PANTONE: str = "#FEDF00"
    YELLOW_PROCESS: str = "#FFEF00"
    YELLOW_RYB: str = "#FEFE33"
    YELLOW_GREEN: str = "#9ACD32"
    YELLOW_GREEN_CRAYOLA: str = "#C5E384"
    YELLOW_GREEN_COLOR_WHEEL: str = "#30B21A"
    YELLOW_ORANGE: str = "#FFAE42"
    YELLOW_ORANGE_COLOR_WHEEL: str = "#FF9505"
    YELLOW_SUNSHINE: str = "#FFF700"
    YINMN_BLUE: str = "#2E5090"
    ZAFFRE: str = "#0014A8"
    ZINNWALDITE_BROWN: str = "#2C1608"
    ZOMP: str = "#39A78E"


class Layer(Enum):
    """
    Supplies enum-based options for different color layers within a terminal, such as Foreground and Background.
    """
    Foreground: int = 38
    Background: int = 48


class Color:
    """
    Utility class handling various color format conversions, including ANSI to RGB, RGB to CMYK, and others.

    Note: Some methods converting to ANSI currently do not support the standard color format.
    """

    @classmethod
    def _validate_layer(cls, layer: Layer) -> None:
        """
        Conducts validation to ensure that the provided layer value conforms to the expected format,
        i.e., it should be of the Layer enum type.
        :param layer: The layer value to be validated, expected to be of the Layer enum type.
        :type layer: Layer
        """
        Validate.validate_type(layer, Layer, 'layer should be of Layer type.')

    @classmethod
    def _hex_distance(cls, hex1: str, hex2: str) -> int:
        """
        Produces the closest RGB color value based on the provided inputs.
        The inputs consist of the HEX code of the standard color and the HEX code to identify the nearest value.
        Note: Exclude the '#' symbol before the HEX codes.
        :param hex1: The HEX code of the standard color.
        :type hex1: str
        :param hex2: The HEX code of the color to find the closest to.
        :type hex2: str
        :return: The integer-based closest RGB value for the provided inputs.
        :rtype: int
        """
        if len(hex1) != 6 or len(hex2) != 6:
            raise ValueError('Hex color values must be of length 6 (excluding # symbol)')

        r1, g1, b1 = tuple(int(hex1[i:i + 2], 16) for i in (0, 2, 4))
        r2, g2, b2 = tuple(int(hex2[i:i + 2], 16) for i in (0, 2, 4))
        return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)

    @classmethod
    def _closest_standard_color(cls, hex_code: str) -> int:
        """
        Generates the nearest RGB color value based on the provided input. The input is a HEX code used
        to identify the closest color. This method utilizes standard colors and the provided HEX code to
        determine the nearest color value.
        :param hex_code: The HEX code of the color to find the closest match to.
        :type hex_code: str
        :return: The integer-based closest RGB value for the provided input.
        :rtype: int
        """
        standard_colors = [
            '000000', '800000', '008000', '808000',
            '000080', '800080', '008080', 'C0C0C0',
            '808080', 'FF0000', '00FF00', 'FFFF00',
            '0000FF', 'FF00FF', '00FFFF', 'FFFFFF'
        ]
        closest_color = min(standard_colors, key=lambda color: cls._hex_distance(hex_code, color))
        return standard_colors.index(closest_color) + 44

    @classmethod
    def hex_to_rgb(cls, hex_code: str) -> tuple[int, int, int]:
        """
        Converts the given color HEX code to RGB format.
        :param hex_code: The HEX code of the color to be converted.
        :type hex_code: str
        :return: The equivalent RGB (red, green, blue) value for the provided input.
        :rtype: tuple(int, int, int)
        """
        Validate.validate_hex(hex_code)

        hex_code = hex_code.lstrip('#')
        return (
            int(hex_code[0:2], 16),
            int(hex_code[2:4], 16),
            int(hex_code[4:6], 16)
        )

    @classmethod
    def rgb_to_hex(cls, r: int, g: int, b: int) -> str:
        """
        Converts the provided RGB (red, green, blue) color values to HEX code format.
        :param r: The red value of the color to be converted.
        :type r: int
        :param g: The green value of the color to be converted.
        :type g: int
        :param b: The blue value of the color to be converted.
        :type b: int
        :return: The equivalent HEX code value for the provided RGB color input.
        :rtype: str
        """
        Validate.validate_rgb(r, g, b)

        return f'#{r:02x}{g:02x}{b:02x}'.upper()

    @classmethod
    def cmyk_to_rgb(cls, c: float, m: float, y: float, k: float) -> tuple[int, int, int]:
        """
        Converts the given CMYK (cyan, magenta, yellow, key) color values to RGB (red, green, blue) format.
        :param c: The cyan value of the color to be converted.
        :type c: float
        :param m: The magenta value of the color to be converted.
        :type m: float
        :param y: The yellow value of the color to be converted.
        :type y: float
        :param k: The key value of the color to be converted.
        :type k: float
        :return: The equivalent RGB color value for the provided CMYK color input.
        :rtype: tuple(int, int, int)
        """
        Validate.validate_cmyk(c, m, y, k)

        return (
            int(255 * (1 - c) * (1 - k)),
            int(255 * (1 - m) * (1 - k)),
            int(255 * (1 - y) * (1 - k))
        )

    @classmethod
    def rgb_to_cmyk(cls, r: int, g: int, b: int) -> tuple[float, float, float, float]:
        """
        Converts the given RGB (red, green, blue) color values to CMYK (cyan, magenta, yellow, key) format.
        :param r: The red value of the color to be converted.
        :type r: int
        :param g: The green value of the color to be converted.
        :type g: int
        :param b: The blue value of the color to be converted.
        :type b: int
        :return: The equivalent CMYK color value for the provided RGB color input.
        :rtype: tuple(float, float, float, float)
        """
        Validate.validate_rgb(r, g, b)

        if (r, g, b) == (0, 0, 0):
            return 0.0, 0.0, 0.0, 1.0

        c = 1 - r / 255
        m = 1 - g / 255
        y = 1 - b / 255
        k = min(c, m, y)
        c = (c - k) / (1 - k)
        m = (m - k) / (1 - k)
        y = (y - k) / (1 - k)

        return c, m, y, k

    @classmethod
    def hex_to_ansi(cls, hex_code: str, layer: Layer, true_color: Optional[bool] = True) -> str:
        """
        Converts a given HEX code color value to ANSI code format.
        Note: If standard color is chosen instead of true color, the closest color value will be returned.
        :param hex_code: The HEX code color value to be converted.
        :type hex_code: str
        :param layer: The layer to which the color should be applied, either Foreground or Background.
        :type layer: Layer
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The equivalent ANSI code color value for the provided HEX code color input value.
        :rtype: str
        """
        Validate.validate_hex(hex_code)
        cls._validate_layer(layer)
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            r, g, b = cls.hex_to_rgb(hex_code)
            return f'\033[{layer.value};2;{r};{g};{b}m'
        else:
            closest_color_code = cls._closest_standard_color(hex_code.lstrip('#'))
            return f'\033[{closest_color_code + layer.value}m'

    @classmethod
    def ansi_to_hex(cls, ansi: str) -> str:
        """
        Converts the provided ANSI code color value to the HEX code color format.
        Note: Conversion from ANSI to HEX for standard colors is not currently supported.
        :param ansi: The ANSI code color to be converted.
        :type ansi: str
        :return: The equivalent HEX code color value for the provided ANSI code color input value.
        :rtype: str
        """
        Validate.validate_ansi(ansi)

        if ansi.startswith('\033[38;2;') or ansi.startswith('\033[48;2;'):
            code = ansi[7:].rstrip('m')
            r, g, b = map(int, code.split(';'))
            return cls.rgb_to_hex(r, g, b)
        else:
            raise Warning('Converting ANSI to HEX for standard colors is not currently supported.')

    @classmethod
    def rgb_to_ansi(cls, r: int, g: int, b: int, layer: Layer, true_color: Optional[bool] = True) -> str:
        """
        Converts the given RGB (red, green, blue) color values to the corresponding HEX code color format.
        :param r: The red value of the color to be converted.
        :type r: int
        :param g: The green value of the color to be converted.
        :type g: int
        :param b: The blue value of the color to be converted.
        :type b: int
        :param layer: The layer to which the color should be applied, either Foreground or Background.
        :type layer: Layer
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The equivalent HEX code color value for the provided RGB color input value.
        :rtype: str
        """
        Validate.validate_rgb(r, g, b)
        cls._validate_layer(layer)
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            return f'\033[{layer.value};2;{r};{g};{b}m'
        else:
            hex_code = cls.rgb_to_hex(r, g, b).lstrip('#')
            closest_color_code = cls._closest_standard_color(hex_code)
            return f'\033[{closest_color_code + layer.value}m'

    @classmethod
    def ansi_to_rgb(cls, ansi: str) -> tuple[int, int, int]:
        """
        Converts the provided ANSI code color value to the RGB (red, green, blue) color format.
        Note: Conversion from ANSI to RGB for standard colors is not currently supported.
        :param ansi: The ANSI code color to be converted.
        :type ansi: str
        :return: The equivalent RGB code color value for the provided ANSI code color input value.
        :rtype: tuple(int, int, int)
        """
        Validate.validate_ansi(ansi)

        if ansi.startswith('\033[38;2;') or ansi.startswith('\033[48;2;'):
            code = ansi[7:].rstrip('m')
            r, g, b = map(int, code.split(';'))
            return r, g, b
        else:
            raise Warning('Converting ANSI to RGB for standard colors is not currently supported.')

    @classmethod
    def cmyk_to_ansi(
            cls, c: float, m: float, y: float, k: float, layer: Layer, true_color: Optional[bool] = True
    ) -> str:
        """
        Converts the given CMYK (cyan, magenta, yellow, key) color values to the corresponding ANSI code color format.
        :param c: The cyan value of the color to be converted.
        :type c: float
        :param m: The magenta value of the color to be converted.
        :type m: float
        :param y: The yellow value of the color to be converted.
        :type y: float
        :param k: The key value of the color to be converted.
        :type k: float
        :param layer: The layer to which the color should be applied, either Foreground or Background.
        :type layer: Layer
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The equivalent ANSI code color value for the provided CMYK color input value.
        :rtype: str
        """
        Validate.validate_cmyk(c, m, y, k)
        cls._validate_layer(layer)
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            r, g, b = cls.cmyk_to_rgb(c, m, y, k)
            return cls.rgb_to_ansi(r, g, b, layer, true_color)
        else:
            r, g, b = cls.cmyk_to_rgb(c, m, y, k)
            hex_code = cls.rgb_to_hex(r, g, b).lstrip('#')
            closest_color_code = cls._closest_standard_color(hex_code)
            return f'\033[{closest_color_code + layer.value}m'

    @classmethod
    def ansi_to_cmyk(cls, ansi: str) -> tuple[float, float, float, float]:
        """
        Converts the provided ANSI code color value to the CMYK (cyan, magenta, yellow, key) color format.
        Note: Conversion from ANSI to CMYK for standard colors is not currently supported.
        :param ansi: The ANSI code color to be converted.
        :type ansi: str
        :return: The equivalent CMYK code color value for the provided ANSI code color input value.
        :rtype: tuple(float, float, float, float)
        """
        try:
            r, g, b = cls.ansi_to_rgb(ansi)
            return cls.rgb_to_cmyk(r, g, b)
        except Warning:
            raise Warning('Converting ANSI to CMYK for standard colors is not currently supported.')


class TextBackgroundColor:
    """
    This class defines text background colors for styling console text within the terminal.
    It includes both standard and true colors. The true colors are sourced from Wikipedia;
    please refer to the licensing information for more details. Additionally, the class offers
    methods to handle custom colors.
    """

    # Standard terminal colors supported by various operating systems
    _standard_colors = {
        'BLACK': "\033[40m",
        'RED': "\033[41m",
        'GREEN': "\033[42m",
        'YELLOW': "\033[43m",
        'BLUE': "\033[44m",
        'MAGENTA': "\033[45m",
        'CYAN': "\033[46m",
        'WHITE': "\033[47m"
    }

    # True colors, also known as 24-bit color, allow for a much broader range of colors than the
    # traditional 8-bit color systems. They enable millions of distinct colors to be displayed,
    # providing more accurate and vibrant representations of images and graphics. However, support
    # for true colors may vary depending on the capabilities of the terminal and the underlying operating system.
    _true_colors = {
        'ABSOLUTE_ZERO': Color.hex_to_ansi(HEXCodes.ABSOLUTE_ZERO, Layer.Background),
        'ACID_GREEN': Color.hex_to_ansi(HEXCodes.ACID_GREEN, Layer.Background),
        'AERO': Color.hex_to_ansi(HEXCodes.AERO, Layer.Background),
        'AFRICAN_VIOLET': Color.hex_to_ansi(HEXCodes.AFRICAN_VIOLET, Layer.Background),
        'AIR_SUPERIORITY_BLUE': Color.hex_to_ansi(HEXCodes.AIR_SUPERIORITY_BLUE, Layer.Background),
        'ALICE_BLUE': Color.hex_to_ansi(HEXCodes.ALICE_BLUE, Layer.Background),
        'ALIZARIN': Color.hex_to_ansi(HEXCodes.ALIZARIN, Layer.Background),
        'ALLOY_ORANGE': Color.hex_to_ansi(HEXCodes.ALLOY_ORANGE, Layer.Background),
        'ALMOND': Color.hex_to_ansi(HEXCodes.ALMOND, Layer.Background),
        'AMARANTH_DEEP_PURPLE': Color.hex_to_ansi(HEXCodes.AMARANTH_DEEP_PURPLE, Layer.Background),
        'AMARANTH_PINK': Color.hex_to_ansi(HEXCodes.AMARANTH_PINK, Layer.Background),
        'AMARANTH_PURPLE': Color.hex_to_ansi(HEXCodes.AMARANTH_PURPLE, Layer.Background),
        'AMAZON': Color.hex_to_ansi(HEXCodes.AMAZON, Layer.Background),
        'AMBER': Color.hex_to_ansi(HEXCodes.AMBER, Layer.Background),
        'AMETHYST': Color.hex_to_ansi(HEXCodes.AMETHYST, Layer.Background),
        'ANDROID_GREEN': Color.hex_to_ansi(HEXCodes.ANDROID_GREEN, Layer.Background),
        'ANTIQUE_BRASS': Color.hex_to_ansi(HEXCodes.ANTIQUE_BRASS, Layer.Background),
        'ANTIQUE_BRONZE': Color.hex_to_ansi(HEXCodes.ANTIQUE_BRONZE, Layer.Background),
        'ANTIQUE_FUCHSIA': Color.hex_to_ansi(HEXCodes.ANTIQUE_FUCHSIA, Layer.Background),
        'ANTIQUE_RUBY': Color.hex_to_ansi(HEXCodes.ANTIQUE_RUBY, Layer.Background),
        'ANTIQUE_WHITE': Color.hex_to_ansi(HEXCodes.ANTIQUE_WHITE, Layer.Background),
        'APRICOT': Color.hex_to_ansi(HEXCodes.APRICOT, Layer.Background),
        'AQUA': Color.hex_to_ansi(HEXCodes.AQUA, Layer.Background),
        'AQUAMARINE': Color.hex_to_ansi(HEXCodes.AQUAMARINE, Layer.Background),
        'ARCTIC_LIME': Color.hex_to_ansi(HEXCodes.ARCTIC_LIME, Layer.Background),
        'ARTICHOKE_GREEN': Color.hex_to_ansi(HEXCodes.ARTICHOKE_GREEN, Layer.Background),
        'ARYLIDE_YELLOW': Color.hex_to_ansi(HEXCodes.ARYLIDE_YELLOW, Layer.Background),
        'ASH_GRAY': Color.hex_to_ansi(HEXCodes.ASH_GRAY, Layer.Background),
        'ATOMIC_TANGERINE': Color.hex_to_ansi(HEXCodes.ATOMIC_TANGERINE, Layer.Background),
        'AUREOLIN': Color.hex_to_ansi(HEXCodes.AUREOLIN, Layer.Background),
        'AZURE': Color.hex_to_ansi(HEXCodes.AZURE, Layer.Background),
        'BABY_BLUE': Color.hex_to_ansi(HEXCodes.BABY_BLUE, Layer.Background),
        'BABY_BLUE_EYES': Color.hex_to_ansi(HEXCodes.BABY_BLUE_EYES, Layer.Background),
        'BABY_PINK': Color.hex_to_ansi(HEXCodes.BABY_PINK, Layer.Background),
        'BABY_POWDER': Color.hex_to_ansi(HEXCodes.BABY_POWDER, Layer.Background),
        'BAKER_MILLER_PINK': Color.hex_to_ansi(HEXCodes.BAKER_MILLER_PINK, Layer.Background),
        'BANANA_MANIA': Color.hex_to_ansi(HEXCodes.BANANA_MANIA, Layer.Background),
        'BARBIE_PINK': Color.hex_to_ansi(HEXCodes.BARBIE_PINK, Layer.Background),
        'BARN_RED': Color.hex_to_ansi(HEXCodes.BARN_RED, Layer.Background),
        'BATTLESHIP_GREY': Color.hex_to_ansi(HEXCodes.BATTLESHIP_GREY, Layer.Background),
        'BEAU_BLUE': Color.hex_to_ansi(HEXCodes.BEAU_BLUE, Layer.Background),
        'BEAVER': Color.hex_to_ansi(HEXCodes.BEAVER, Layer.Background),
        'BEIGE': Color.hex_to_ansi(HEXCodes.BEIGE, Layer.Background),
        'B_DAZZLED_BLUE': Color.hex_to_ansi(HEXCodes.B_DAZZLED_BLUE, Layer.Background),
        'BIG_DIP_O_RUBY': Color.hex_to_ansi(HEXCodes.BIG_DIP_O_RUBY, Layer.Background),
        'BISQUE': Color.hex_to_ansi(HEXCodes.BISQUE, Layer.Background),
        'BISTRE': Color.hex_to_ansi(HEXCodes.BISTRE, Layer.Background),
        'BISTRE_BROWN': Color.hex_to_ansi(HEXCodes.BISTRE_BROWN, Layer.Background),
        'BITTER_LEMON': Color.hex_to_ansi(HEXCodes.BITTER_LEMON, Layer.Background),
        'BLACK_BEAN': Color.hex_to_ansi(HEXCodes.BLACK_BEAN, Layer.Background),
        'BLACK_CORAL': Color.hex_to_ansi(HEXCodes.BLACK_CORAL, Layer.Background),
        'BLACK_OLIVE': Color.hex_to_ansi(HEXCodes.BLACK_OLIVE, Layer.Background),
        'BLACK_SHADOWS': Color.hex_to_ansi(HEXCodes.BLACK_SHADOWS, Layer.Background),
        'BLANCHED_ALMOND': Color.hex_to_ansi(HEXCodes.BLANCHED_ALMOND, Layer.Background),
        'BLAST_OFF_BRONZE': Color.hex_to_ansi(HEXCodes.BLAST_OFF_BRONZE, Layer.Background),
        'BLEU_DE_FRANCE': Color.hex_to_ansi(HEXCodes.BLEU_DE_FRANCE, Layer.Background),
        'BLIZZARD_BLUE': Color.hex_to_ansi(HEXCodes.BLIZZARD_BLUE, Layer.Background),
        'BLOOD_RED': Color.hex_to_ansi(HEXCodes.BLOOD_RED, Layer.Background),
        'BLUE_CRAYOLA': Color.hex_to_ansi(HEXCodes.BLUE_CRAYOLA, Layer.Background),
        'BLUE_MUNSELL': Color.hex_to_ansi(HEXCodes.BLUE_MUNSELL, Layer.Background),
        'BLUE_NCS': Color.hex_to_ansi(HEXCodes.BLUE_NCS, Layer.Background),
        'BLUE_PANTONE': Color.hex_to_ansi(HEXCodes.BLUE_PANTONE, Layer.Background),
        'BLUE_PIGMENT': Color.hex_to_ansi(HEXCodes.BLUE_PIGMENT, Layer.Background),
        'BLUE_BELL': Color.hex_to_ansi(HEXCodes.BLUE_BELL, Layer.Background),
        'BLUE_GRAY_CRAYOLA': Color.hex_to_ansi(HEXCodes.BLUE_GRAY_CRAYOLA, Layer.Background),
        'BLUE_JEANS': Color.hex_to_ansi(HEXCodes.BLUE_JEANS, Layer.Background),
        'BLUE_SAPPHIRE': Color.hex_to_ansi(HEXCodes.BLUE_SAPPHIRE, Layer.Background),
        'BLUE_VIOLET': Color.hex_to_ansi(HEXCodes.BLUE_VIOLET, Layer.Background),
        'BLUE_YONDER': Color.hex_to_ansi(HEXCodes.BLUE_YONDER, Layer.Background),
        'BLUETIFUL': Color.hex_to_ansi(HEXCodes.BLUETIFUL, Layer.Background),
        'BLUSH': Color.hex_to_ansi(HEXCodes.BLUSH, Layer.Background),
        'BOLE': Color.hex_to_ansi(HEXCodes.BOLE, Layer.Background),
        'BONE': Color.hex_to_ansi(HEXCodes.BONE, Layer.Background),
        'BRICK_RED': Color.hex_to_ansi(HEXCodes.BRICK_RED, Layer.Background),
        'BRIGHT_LILAC': Color.hex_to_ansi(HEXCodes.BRIGHT_LILAC, Layer.Background),
        'BRIGHT_YELLOW_CRAYOLA': Color.hex_to_ansi(HEXCodes.BRIGHT_YELLOW_CRAYOLA, Layer.Background),
        'BRITISH_RACING_GREEN': Color.hex_to_ansi(HEXCodes.BRITISH_RACING_GREEN, Layer.Background),
        'BRONZE': Color.hex_to_ansi(HEXCodes.BRONZE, Layer.Background),
        'BROWN': Color.hex_to_ansi(HEXCodes.BROWN, Layer.Background),
        'BROWN_SUGAR': Color.hex_to_ansi(HEXCodes.BROWN_SUGAR, Layer.Background),
        'BUD_GREEN': Color.hex_to_ansi(HEXCodes.BUD_GREEN, Layer.Background),
        'BUFF': Color.hex_to_ansi(HEXCodes.BUFF, Layer.Background),
        'BURGUNDY': Color.hex_to_ansi(HEXCodes.BURGUNDY, Layer.Background),
        'BURLYWOOD': Color.hex_to_ansi(HEXCodes.BURLYWOOD, Layer.Background),
        'BURNISHED_BROWN': Color.hex_to_ansi(HEXCodes.BURNISHED_BROWN, Layer.Background),
        'BURNT_ORANGE': Color.hex_to_ansi(HEXCodes.BURNT_ORANGE, Layer.Background),
        'BURNT_SIENNA': Color.hex_to_ansi(HEXCodes.BURNT_SIENNA, Layer.Background),
        'BURNT_UMBER': Color.hex_to_ansi(HEXCodes.BURNT_UMBER, Layer.Background),
        'BYZANTINE': Color.hex_to_ansi(HEXCodes.BYZANTINE, Layer.Background),
        'BYZANTIUM': Color.hex_to_ansi(HEXCodes.BYZANTIUM, Layer.Background),
        'CADET_BLUE': Color.hex_to_ansi(HEXCodes.CADET_BLUE, Layer.Background),
        'CADET_GREY': Color.hex_to_ansi(HEXCodes.CADET_GREY, Layer.Background),
        'CADMIUM_GREEN': Color.hex_to_ansi(HEXCodes.CADMIUM_GREEN, Layer.Background),
        'CADMIUM_ORANGE': Color.hex_to_ansi(HEXCodes.CADMIUM_ORANGE, Layer.Background),
        'CAFE_AU_LAIT': Color.hex_to_ansi(HEXCodes.CAFE_AU_LAIT, Layer.Background),
        'CAFE_NOIR': Color.hex_to_ansi(HEXCodes.CAFE_NOIR, Layer.Background),
        'CAMBRIDGE_BLUE': Color.hex_to_ansi(HEXCodes.CAMBRIDGE_BLUE, Layer.Background),
        'CAMEL': Color.hex_to_ansi(HEXCodes.CAMEL, Layer.Background),
        'CAMEO_PINK': Color.hex_to_ansi(HEXCodes.CAMEO_PINK, Layer.Background),
        'CANARY': Color.hex_to_ansi(HEXCodes.CANARY, Layer.Background),
        'CANARY_YELLOW': Color.hex_to_ansi(HEXCodes.CANARY_YELLOW, Layer.Background),
        'CANDY_PINK': Color.hex_to_ansi(HEXCodes.CANDY_PINK, Layer.Background),
        'CARDINAL': Color.hex_to_ansi(HEXCodes.CARDINAL, Layer.Background),
        'CARIBBEAN_GREEN': Color.hex_to_ansi(HEXCodes.CARIBBEAN_GREEN, Layer.Background),
        'CARMINE': Color.hex_to_ansi(HEXCodes.CARMINE, Layer.Background),
        'CARMINE_M_P': Color.hex_to_ansi(HEXCodes.CARMINE_M_P, Layer.Background),
        'CARNATION_PINK': Color.hex_to_ansi(HEXCodes.CARNATION_PINK, Layer.Background),
        'CARNELIAN': Color.hex_to_ansi(HEXCodes.CARNELIAN, Layer.Background),
        'CAROLINA_BLUE': Color.hex_to_ansi(HEXCodes.CAROLINA_BLUE, Layer.Background),
        'CARROT_ORANGE': Color.hex_to_ansi(HEXCodes.CARROT_ORANGE, Layer.Background),
        'CATAWBA': Color.hex_to_ansi(HEXCodes.CATAWBA, Layer.Background),
        'CEDAR_CHEST': Color.hex_to_ansi(HEXCodes.CEDAR_CHEST, Layer.Background),
        'CELADON': Color.hex_to_ansi(HEXCodes.CELADON, Layer.Background),
        'CELESTE': Color.hex_to_ansi(HEXCodes.CELESTE, Layer.Background),
        'CERISE': Color.hex_to_ansi(HEXCodes.CERISE, Layer.Background),
        'CERULEAN': Color.hex_to_ansi(HEXCodes.CERULEAN, Layer.Background),
        'CERULEAN_BLUE': Color.hex_to_ansi(HEXCodes.CERULEAN_BLUE, Layer.Background),
        'CERULEAN_FROST': Color.hex_to_ansi(HEXCodes.CERULEAN_FROST, Layer.Background),
        'CERULEAN_CRAYOLA': Color.hex_to_ansi(HEXCodes.CERULEAN_CRAYOLA, Layer.Background),
        'CERULEAN_RGB': Color.hex_to_ansi(HEXCodes.CERULEAN_RGB, Layer.Background),
        'CHAMPAGNE': Color.hex_to_ansi(HEXCodes.CHAMPAGNE, Layer.Background),
        'CHAMPAGNE_PINK': Color.hex_to_ansi(HEXCodes.CHAMPAGNE_PINK, Layer.Background),
        'CHARCOAL': Color.hex_to_ansi(HEXCodes.CHARCOAL, Layer.Background),
        'CHARM_PINK': Color.hex_to_ansi(HEXCodes.CHARM_PINK, Layer.Background),
        'CHARTREUSE_WEB': Color.hex_to_ansi(HEXCodes.CHARTREUSE_WEB, Layer.Background),
        'CHERRY_BLOSSOM_PINK': Color.hex_to_ansi(HEXCodes.CHERRY_BLOSSOM_PINK, Layer.Background),
        'CHESTNUT': Color.hex_to_ansi(HEXCodes.CHESTNUT, Layer.Background),
        'CHILI_RED': Color.hex_to_ansi(HEXCodes.CHILI_RED, Layer.Background),
        'CHINA_PINK': Color.hex_to_ansi(HEXCodes.CHINA_PINK, Layer.Background),
        'CHINESE_RED': Color.hex_to_ansi(HEXCodes.CHINESE_RED, Layer.Background),
        'CHINESE_VIOLET': Color.hex_to_ansi(HEXCodes.CHINESE_VIOLET, Layer.Background),
        'CHINESE_YELLOW': Color.hex_to_ansi(HEXCodes.CHINESE_YELLOW, Layer.Background),
        'CHOCOLATE_TRADITIONAL': Color.hex_to_ansi(HEXCodes.CHOCOLATE_TRADITIONAL, Layer.Background),
        'CHOCOLATE_WEB': Color.hex_to_ansi(HEXCodes.CHOCOLATE_WEB, Layer.Background),
        'CINEREOUS': Color.hex_to_ansi(HEXCodes.CINEREOUS, Layer.Background),
        'CINNABAR': Color.hex_to_ansi(HEXCodes.CINNABAR, Layer.Background),
        'CINNAMON_SATIN': Color.hex_to_ansi(HEXCodes.CINNAMON_SATIN, Layer.Background),
        'CITRINE': Color.hex_to_ansi(HEXCodes.CITRINE, Layer.Background),
        'CITRON': Color.hex_to_ansi(HEXCodes.CITRON, Layer.Background),
        'CLARET': Color.hex_to_ansi(HEXCodes.CLARET, Layer.Background),
        'COFFEE': Color.hex_to_ansi(HEXCodes.COFFEE, Layer.Background),
        'COLUMBIA_BLUE': Color.hex_to_ansi(HEXCodes.COLUMBIA_BLUE, Layer.Background),
        'CONGO_PINK': Color.hex_to_ansi(HEXCodes.CONGO_PINK, Layer.Background),
        'COOL_GREY': Color.hex_to_ansi(HEXCodes.COOL_GREY, Layer.Background),
        'COPPER': Color.hex_to_ansi(HEXCodes.COPPER, Layer.Background),
        'COPPER_CRAYOLA': Color.hex_to_ansi(HEXCodes.COPPER_CRAYOLA, Layer.Background),
        'COPPER_PENNY': Color.hex_to_ansi(HEXCodes.COPPER_PENNY, Layer.Background),
        'COPPER_RED': Color.hex_to_ansi(HEXCodes.COPPER_RED, Layer.Background),
        'COPPER_ROSE': Color.hex_to_ansi(HEXCodes.COPPER_ROSE, Layer.Background),
        'COQUELICOT': Color.hex_to_ansi(HEXCodes.COQUELICOT, Layer.Background),
        'CORAL': Color.hex_to_ansi(HEXCodes.CORAL, Layer.Background),
        'CORAL_PINK': Color.hex_to_ansi(HEXCodes.CORAL_PINK, Layer.Background),
        'CORDOVAN': Color.hex_to_ansi(HEXCodes.CORDOVAN, Layer.Background),
        'CORN': Color.hex_to_ansi(HEXCodes.CORN, Layer.Background),
        'CORNFLOWER_BLUE': Color.hex_to_ansi(HEXCodes.CORNFLOWER_BLUE, Layer.Background),
        'CORNSILK': Color.hex_to_ansi(HEXCodes.CORNSILK, Layer.Background),
        'COSMIC_COBALT': Color.hex_to_ansi(HEXCodes.COSMIC_COBALT, Layer.Background),
        'COSMIC_LATTE': Color.hex_to_ansi(HEXCodes.COSMIC_LATTE, Layer.Background),
        'COYOTE_BROWN': Color.hex_to_ansi(HEXCodes.COYOTE_BROWN, Layer.Background),
        'COTTON_CANDY': Color.hex_to_ansi(HEXCodes.COTTON_CANDY, Layer.Background),
        'CREAM': Color.hex_to_ansi(HEXCodes.CREAM, Layer.Background),
        'CRIMSON': Color.hex_to_ansi(HEXCodes.CRIMSON, Layer.Background),
        'CRIMSON_UA': Color.hex_to_ansi(HEXCodes.CRIMSON_UA, Layer.Background),
        'CULTURED_PEARL': Color.hex_to_ansi(HEXCodes.CULTURED_PEARL, Layer.Background),
        'CYAN_PROCESS': Color.hex_to_ansi(HEXCodes.CYAN_PROCESS, Layer.Background),
        'CYBER_GRAPE': Color.hex_to_ansi(HEXCodes.CYBER_GRAPE, Layer.Background),
        'CYBER_YELLOW': Color.hex_to_ansi(HEXCodes.CYBER_YELLOW, Layer.Background),
        'CYCLAMEN': Color.hex_to_ansi(HEXCodes.CYCLAMEN, Layer.Background),
        'DANDELION': Color.hex_to_ansi(HEXCodes.DANDELION, Layer.Background),
        'DARK_BROWN': Color.hex_to_ansi(HEXCodes.DARK_BROWN, Layer.Background),
        'DARK_BYZANTIUM': Color.hex_to_ansi(HEXCodes.DARK_BYZANTIUM, Layer.Background),
        'DARK_CYAN': Color.hex_to_ansi(HEXCodes.DARK_CYAN, Layer.Background),
        'DARK_ELECTRIC_BLUE': Color.hex_to_ansi(HEXCodes.DARK_ELECTRIC_BLUE, Layer.Background),
        'DARK_GOLDENROD': Color.hex_to_ansi(HEXCodes.DARK_GOLDENROD, Layer.Background),
        'DARK_GREEN_X11': Color.hex_to_ansi(HEXCodes.DARK_GREEN_X11, Layer.Background),
        'DARK_JUNGLE_GREEN': Color.hex_to_ansi(HEXCodes.DARK_JUNGLE_GREEN, Layer.Background),
        'DARK_KHAKI': Color.hex_to_ansi(HEXCodes.DARK_KHAKI, Layer.Background),
        'DARK_LAVA': Color.hex_to_ansi(HEXCodes.DARK_LAVA, Layer.Background),
        'DARK_LIVER_HORSES': Color.hex_to_ansi(HEXCodes.DARK_LIVER_HORSES, Layer.Background),
        'DARK_MAGENTA': Color.hex_to_ansi(HEXCodes.DARK_MAGENTA, Layer.Background),
        'DARK_OLIVE_GREEN': Color.hex_to_ansi(HEXCodes.DARK_OLIVE_GREEN, Layer.Background),
        'DARK_ORANGE': Color.hex_to_ansi(HEXCodes.DARK_ORANGE, Layer.Background),
        'DARK_ORCHID': Color.hex_to_ansi(HEXCodes.DARK_ORCHID, Layer.Background),
        'DARK_PURPLE': Color.hex_to_ansi(HEXCodes.DARK_PURPLE, Layer.Background),
        'DARK_RED': Color.hex_to_ansi(HEXCodes.DARK_RED, Layer.Background),
        'DARK_SALMON': Color.hex_to_ansi(HEXCodes.DARK_SALMON, Layer.Background),
        'DARK_SEA_GREEN': Color.hex_to_ansi(HEXCodes.DARK_SEA_GREEN, Layer.Background),
        'DARK_SIENNA': Color.hex_to_ansi(HEXCodes.DARK_SIENNA, Layer.Background),
        'DARK_SKY_BLUE': Color.hex_to_ansi(HEXCodes.DARK_SKY_BLUE, Layer.Background),
        'DARK_SLATE_BLUE': Color.hex_to_ansi(HEXCodes.DARK_SLATE_BLUE, Layer.Background),
        'DARK_SLATE_GRAY': Color.hex_to_ansi(HEXCodes.DARK_SLATE_GRAY, Layer.Background),
        'DARK_SPRING_GREEN': Color.hex_to_ansi(HEXCodes.DARK_SPRING_GREEN, Layer.Background),
        'DARK_TURQUOISE': Color.hex_to_ansi(HEXCodes.DARK_TURQUOISE, Layer.Background),
        'DARK_VIOLET': Color.hex_to_ansi(HEXCodes.DARK_VIOLET, Layer.Background),
        'DAVY_S_GREY': Color.hex_to_ansi(HEXCodes.DAVY_S_GREY, Layer.Background),
        'DEEP_CERISE': Color.hex_to_ansi(HEXCodes.DEEP_CERISE, Layer.Background),
        'DEEP_CHAMPAGNE': Color.hex_to_ansi(HEXCodes.DEEP_CHAMPAGNE, Layer.Background),
        'DEEP_CHESTNUT': Color.hex_to_ansi(HEXCodes.DEEP_CHESTNUT, Layer.Background),
        'DEEP_JUNGLE_GREEN': Color.hex_to_ansi(HEXCodes.DEEP_JUNGLE_GREEN, Layer.Background),
        'DEEP_PINK': Color.hex_to_ansi(HEXCodes.DEEP_PINK, Layer.Background),
        'DEEP_SAFFRON': Color.hex_to_ansi(HEXCodes.DEEP_SAFFRON, Layer.Background),
        'DEEP_SKY_BLUE': Color.hex_to_ansi(HEXCodes.DEEP_SKY_BLUE, Layer.Background),
        'DEEP_SPACE_SPARKLE': Color.hex_to_ansi(HEXCodes.DEEP_SPACE_SPARKLE, Layer.Background),
        'DEEP_TAUPE': Color.hex_to_ansi(HEXCodes.DEEP_TAUPE, Layer.Background),
        'DENIM': Color.hex_to_ansi(HEXCodes.DENIM, Layer.Background),
        'DENIM_BLUE': Color.hex_to_ansi(HEXCodes.DENIM_BLUE, Layer.Background),
        'DESERT': Color.hex_to_ansi(HEXCodes.DESERT, Layer.Background),
        'DESERT_SAND': Color.hex_to_ansi(HEXCodes.DESERT_SAND, Layer.Background),
        'DIM_GRAY': Color.hex_to_ansi(HEXCodes.DIM_GRAY, Layer.Background),
        'DODGER_BLUE': Color.hex_to_ansi(HEXCodes.DODGER_BLUE, Layer.Background),
        'DRAB_DARK_BROWN': Color.hex_to_ansi(HEXCodes.DRAB_DARK_BROWN, Layer.Background),
        'DUKE_BLUE': Color.hex_to_ansi(HEXCodes.DUKE_BLUE, Layer.Background),
        'DUTCH_WHITE': Color.hex_to_ansi(HEXCodes.DUTCH_WHITE, Layer.Background),
        'EBONY': Color.hex_to_ansi(HEXCodes.EBONY, Layer.Background),
        'ECRU': Color.hex_to_ansi(HEXCodes.ECRU, Layer.Background),
        'EERIE_BLACK': Color.hex_to_ansi(HEXCodes.EERIE_BLACK, Layer.Background),
        'EGGPLANT': Color.hex_to_ansi(HEXCodes.EGGPLANT, Layer.Background),
        'EGGSHELL': Color.hex_to_ansi(HEXCodes.EGGSHELL, Layer.Background),
        'ELECTRIC_LIME': Color.hex_to_ansi(HEXCodes.ELECTRIC_LIME, Layer.Background),
        'ELECTRIC_PURPLE': Color.hex_to_ansi(HEXCodes.ELECTRIC_PURPLE, Layer.Background),
        'ELECTRIC_VIOLET': Color.hex_to_ansi(HEXCodes.ELECTRIC_VIOLET, Layer.Background),
        'EMERALD': Color.hex_to_ansi(HEXCodes.EMERALD, Layer.Background),
        'EMINENCE': Color.hex_to_ansi(HEXCodes.EMINENCE, Layer.Background),
        'ENGLISH_LAVENDER': Color.hex_to_ansi(HEXCodes.ENGLISH_LAVENDER, Layer.Background),
        'ENGLISH_RED': Color.hex_to_ansi(HEXCodes.ENGLISH_RED, Layer.Background),
        'ENGLISH_VERMILLION': Color.hex_to_ansi(HEXCodes.ENGLISH_VERMILLION, Layer.Background),
        'ENGLISH_VIOLET': Color.hex_to_ansi(HEXCodes.ENGLISH_VIOLET, Layer.Background),
        'ERIN': Color.hex_to_ansi(HEXCodes.ERIN, Layer.Background),
        'ETON_BLUE': Color.hex_to_ansi(HEXCodes.ETON_BLUE, Layer.Background),
        'FALLOW': Color.hex_to_ansi(HEXCodes.FALLOW, Layer.Background),
        'FALU_RED': Color.hex_to_ansi(HEXCodes.FALU_RED, Layer.Background),
        'FANDANGO': Color.hex_to_ansi(HEXCodes.FANDANGO, Layer.Background),
        'FANDANGO_PINK': Color.hex_to_ansi(HEXCodes.FANDANGO_PINK, Layer.Background),
        'FAWN': Color.hex_to_ansi(HEXCodes.FAWN, Layer.Background),
        'FERN_GREEN': Color.hex_to_ansi(HEXCodes.FERN_GREEN, Layer.Background),
        'FIELD_DRAB': Color.hex_to_ansi(HEXCodes.FIELD_DRAB, Layer.Background),
        'FIERY_ROSE': Color.hex_to_ansi(HEXCodes.FIERY_ROSE, Layer.Background),
        'FINN': Color.hex_to_ansi(HEXCodes.FINN, Layer.Background),
        'FIREBRICK': Color.hex_to_ansi(HEXCodes.FIREBRICK, Layer.Background),
        'FIRE_ENGINE_RED': Color.hex_to_ansi(HEXCodes.FIRE_ENGINE_RED, Layer.Background),
        'FLAME': Color.hex_to_ansi(HEXCodes.FLAME, Layer.Background),
        'FLAX': Color.hex_to_ansi(HEXCodes.FLAX, Layer.Background),
        'FLIRT': Color.hex_to_ansi(HEXCodes.FLIRT, Layer.Background),
        'FLORAL_WHITE': Color.hex_to_ansi(HEXCodes.FLORAL_WHITE, Layer.Background),
        'FOREST_GREEN_WEB': Color.hex_to_ansi(HEXCodes.FOREST_GREEN_WEB, Layer.Background),
        'FRENCH_BEIGE': Color.hex_to_ansi(HEXCodes.FRENCH_BEIGE, Layer.Background),
        'FRENCH_BISTRE': Color.hex_to_ansi(HEXCodes.FRENCH_BISTRE, Layer.Background),
        'FRENCH_BLUE': Color.hex_to_ansi(HEXCodes.FRENCH_BLUE, Layer.Background),
        'FRENCH_FUCHSIA': Color.hex_to_ansi(HEXCodes.FRENCH_FUCHSIA, Layer.Background),
        'FRENCH_LILAC': Color.hex_to_ansi(HEXCodes.FRENCH_LILAC, Layer.Background),
        'FRENCH_LIME': Color.hex_to_ansi(HEXCodes.FRENCH_LIME, Layer.Background),
        'FRENCH_MAUVE': Color.hex_to_ansi(HEXCodes.FRENCH_MAUVE, Layer.Background),
        'FRENCH_PINK': Color.hex_to_ansi(HEXCodes.FRENCH_PINK, Layer.Background),
        'FRENCH_RASPBERRY': Color.hex_to_ansi(HEXCodes.FRENCH_RASPBERRY, Layer.Background),
        'FRENCH_SKY_BLUE': Color.hex_to_ansi(HEXCodes.FRENCH_SKY_BLUE, Layer.Background),
        'FRENCH_VIOLET': Color.hex_to_ansi(HEXCodes.FRENCH_VIOLET, Layer.Background),
        'FROSTBITE': Color.hex_to_ansi(HEXCodes.FROSTBITE, Layer.Background),
        'FUCHSIA': Color.hex_to_ansi(HEXCodes.FUCHSIA, Layer.Background),
        'FUCHSIA_CRAYOLA': Color.hex_to_ansi(HEXCodes.FUCHSIA_CRAYOLA, Layer.Background),
        'FULVOUS': Color.hex_to_ansi(HEXCodes.FULVOUS, Layer.Background),
        'FUZZY_WUZZY': Color.hex_to_ansi(HEXCodes.FUZZY_WUZZY, Layer.Background),
        'GAINSBORO': Color.hex_to_ansi(HEXCodes.GAINSBORO, Layer.Background),
        'GAMBOGE': Color.hex_to_ansi(HEXCodes.GAMBOGE, Layer.Background),
        'GENERIC_VIRIDIAN': Color.hex_to_ansi(HEXCodes.GENERIC_VIRIDIAN, Layer.Background),
        'GHOST_WHITE': Color.hex_to_ansi(HEXCodes.GHOST_WHITE, Layer.Background),
        'GLAUCOUS': Color.hex_to_ansi(HEXCodes.GLAUCOUS, Layer.Background),
        'GLOSSY_GRAPE': Color.hex_to_ansi(HEXCodes.GLOSSY_GRAPE, Layer.Background),
        'GO_GREEN': Color.hex_to_ansi(HEXCodes.GO_GREEN, Layer.Background),
        'GOLD_METALLIC': Color.hex_to_ansi(HEXCodes.GOLD_METALLIC, Layer.Background),
        'GOLD_WEB_GOLDEN': Color.hex_to_ansi(HEXCodes.GOLD_WEB_GOLDEN, Layer.Background),
        'GOLD_CRAYOLA': Color.hex_to_ansi(HEXCodes.GOLD_CRAYOLA, Layer.Background),
        'GOLD_FUSION': Color.hex_to_ansi(HEXCodes.GOLD_FUSION, Layer.Background),
        'GOLDEN_BROWN': Color.hex_to_ansi(HEXCodes.GOLDEN_BROWN, Layer.Background),
        'GOLDEN_POPPY': Color.hex_to_ansi(HEXCodes.GOLDEN_POPPY, Layer.Background),
        'GOLDEN_YELLOW': Color.hex_to_ansi(HEXCodes.GOLDEN_YELLOW, Layer.Background),
        'GOLDENROD': Color.hex_to_ansi(HEXCodes.GOLDENROD, Layer.Background),
        'GOTHAM_GREEN': Color.hex_to_ansi(HEXCodes.GOTHAM_GREEN, Layer.Background),
        'GRANITE_GRAY': Color.hex_to_ansi(HEXCodes.GRANITE_GRAY, Layer.Background),
        'GRANNY_SMITH_APPLE': Color.hex_to_ansi(HEXCodes.GRANNY_SMITH_APPLE, Layer.Background),
        'GRAY_WEB': Color.hex_to_ansi(HEXCodes.GRAY_WEB, Layer.Background),
        'GRAY_X11_GRAY': Color.hex_to_ansi(HEXCodes.GRAY_X11_GRAY, Layer.Background),
        'GREEN_CRAYOLA': Color.hex_to_ansi(HEXCodes.GREEN_CRAYOLA, Layer.Background),
        'GREEN_WEB': Color.hex_to_ansi(HEXCodes.GREEN_WEB, Layer.Background),
        'GREEN_MUNSELL': Color.hex_to_ansi(HEXCodes.GREEN_MUNSELL, Layer.Background),
        'GREEN_NCS': Color.hex_to_ansi(HEXCodes.GREEN_NCS, Layer.Background),
        'GREEN_PANTONE': Color.hex_to_ansi(HEXCodes.GREEN_PANTONE, Layer.Background),
        'GREEN_PIGMENT': Color.hex_to_ansi(HEXCodes.GREEN_PIGMENT, Layer.Background),
        'GREEN_BLUE': Color.hex_to_ansi(HEXCodes.GREEN_BLUE, Layer.Background),
        'GREEN_LIZARD': Color.hex_to_ansi(HEXCodes.GREEN_LIZARD, Layer.Background),
        'GREEN_SHEEN': Color.hex_to_ansi(HEXCodes.GREEN_SHEEN, Layer.Background),
        'GUNMETAL': Color.hex_to_ansi(HEXCodes.GUNMETAL, Layer.Background),
        'HANSA_YELLOW': Color.hex_to_ansi(HEXCodes.HANSA_YELLOW, Layer.Background),
        'HARLEQUIN': Color.hex_to_ansi(HEXCodes.HARLEQUIN, Layer.Background),
        'HARVEST_GOLD': Color.hex_to_ansi(HEXCodes.HARVEST_GOLD, Layer.Background),
        'HEAT_WAVE': Color.hex_to_ansi(HEXCodes.HEAT_WAVE, Layer.Background),
        'HELIOTROPE': Color.hex_to_ansi(HEXCodes.HELIOTROPE, Layer.Background),
        'HELIOTROPE_GRAY': Color.hex_to_ansi(HEXCodes.HELIOTROPE_GRAY, Layer.Background),
        'HOLLYWOOD_CERISE': Color.hex_to_ansi(HEXCodes.HOLLYWOOD_CERISE, Layer.Background),
        'HONOLULU_BLUE': Color.hex_to_ansi(HEXCodes.HONOLULU_BLUE, Layer.Background),
        'HOOKER_S_GREEN': Color.hex_to_ansi(HEXCodes.HOOKER_S_GREEN, Layer.Background),
        'HOT_MAGENTA': Color.hex_to_ansi(HEXCodes.HOT_MAGENTA, Layer.Background),
        'HOT_PINK': Color.hex_to_ansi(HEXCodes.HOT_PINK, Layer.Background),
        'HUNTER_GREEN': Color.hex_to_ansi(HEXCodes.HUNTER_GREEN, Layer.Background),
        'ICEBERG': Color.hex_to_ansi(HEXCodes.ICEBERG, Layer.Background),
        'ILLUMINATING_EMERALD': Color.hex_to_ansi(HEXCodes.ILLUMINATING_EMERALD, Layer.Background),
        'IMPERIAL_RED': Color.hex_to_ansi(HEXCodes.IMPERIAL_RED, Layer.Background),
        'INCHWORM': Color.hex_to_ansi(HEXCodes.INCHWORM, Layer.Background),
        'INDEPENDENCE': Color.hex_to_ansi(HEXCodes.INDEPENDENCE, Layer.Background),
        'INDIA_GREEN': Color.hex_to_ansi(HEXCodes.INDIA_GREEN, Layer.Background),
        'INDIAN_RED': Color.hex_to_ansi(HEXCodes.INDIAN_RED, Layer.Background),
        'INDIAN_YELLOW': Color.hex_to_ansi(HEXCodes.INDIAN_YELLOW, Layer.Background),
        'INDIGO': Color.hex_to_ansi(HEXCodes.INDIGO, Layer.Background),
        'INDIGO_DYE': Color.hex_to_ansi(HEXCodes.INDIGO_DYE, Layer.Background),
        'INTERNATIONAL_KLEIN_BLUE': Color.hex_to_ansi(HEXCodes.INTERNATIONAL_KLEIN_BLUE, Layer.Background),
        'INTERNATIONAL_ORANGE_ENGINEERING': Color.hex_to_ansi(
            HEXCodes.INTERNATIONAL_ORANGE_ENGINEERING, Layer.Background
        ),
        'INTERNATIONAL_ORANGE_GOLDEN_GATE_BRIDGE': Color.hex_to_ansi(
            HEXCodes.INTERNATIONAL_ORANGE_GOLDEN_GATE_BRIDGE, Layer.Background
        ),
        'IRRESISTIBLE': Color.hex_to_ansi(HEXCodes.IRRESISTIBLE, Layer.Background),
        'ISABELLINE': Color.hex_to_ansi(HEXCodes.ISABELLINE, Layer.Background),
        'ITALIAN_SKY_BLUE': Color.hex_to_ansi(HEXCodes.ITALIAN_SKY_BLUE, Layer.Background),
        'IVORY': Color.hex_to_ansi(HEXCodes.IVORY, Layer.Background),
        'JAPANESE_CARMINE': Color.hex_to_ansi(HEXCodes.JAPANESE_CARMINE, Layer.Background),
        'JAPANESE_VIOLET': Color.hex_to_ansi(HEXCodes.JAPANESE_VIOLET, Layer.Background),
        'JASMINE': Color.hex_to_ansi(HEXCodes.JASMINE, Layer.Background),
        'JAZZBERRY_JAM': Color.hex_to_ansi(HEXCodes.JAZZBERRY_JAM, Layer.Background),
        'JET': Color.hex_to_ansi(HEXCodes.JET, Layer.Background),
        'JONQUIL': Color.hex_to_ansi(HEXCodes.JONQUIL, Layer.Background),
        'JUNE_BUD': Color.hex_to_ansi(HEXCodes.JUNE_BUD, Layer.Background),
        'JUNGLE_GREEN': Color.hex_to_ansi(HEXCodes.JUNGLE_GREEN, Layer.Background),
        'KELLY_GREEN': Color.hex_to_ansi(HEXCodes.KELLY_GREEN, Layer.Background),
        'KEPPEL': Color.hex_to_ansi(HEXCodes.KEPPEL, Layer.Background),
        'KEY_LIME': Color.hex_to_ansi(HEXCodes.KEY_LIME, Layer.Background),
        'KHAKI_WEB': Color.hex_to_ansi(HEXCodes.KHAKI_WEB, Layer.Background),
        'KHAKI_X11_LIGHT_KHAKI': Color.hex_to_ansi(HEXCodes.KHAKI_X11_LIGHT_KHAKI, Layer.Background),
        'KOBE': Color.hex_to_ansi(HEXCodes.KOBE, Layer.Background),
        'KOBI': Color.hex_to_ansi(HEXCodes.KOBI, Layer.Background),
        'KOBICHA': Color.hex_to_ansi(HEXCodes.KOBICHA, Layer.Background),
        'KSU_PURPLE': Color.hex_to_ansi(HEXCodes.KSU_PURPLE, Layer.Background),
        'LANGUID_LAVENDER': Color.hex_to_ansi(HEXCodes.LANGUID_LAVENDER, Layer.Background),
        'LAPIS_LAZULI': Color.hex_to_ansi(HEXCodes.LAPIS_LAZULI, Layer.Background),
        'LASER_LEMON': Color.hex_to_ansi(HEXCodes.LASER_LEMON, Layer.Background),
        'LAUREL_GREEN': Color.hex_to_ansi(HEXCodes.LAUREL_GREEN, Layer.Background),
        'LAVA': Color.hex_to_ansi(HEXCodes.LAVA, Layer.Background),
        'LAVENDER_FLORAL': Color.hex_to_ansi(HEXCodes.LAVENDER_FLORAL, Layer.Background),
        'LAVENDER_WEB': Color.hex_to_ansi(HEXCodes.LAVENDER_WEB, Layer.Background),
        'LAVENDER_BLUE': Color.hex_to_ansi(HEXCodes.LAVENDER_BLUE, Layer.Background),
        'LAVENDER_BLUSH': Color.hex_to_ansi(HEXCodes.LAVENDER_BLUSH, Layer.Background),
        'LAVENDER_GRAY': Color.hex_to_ansi(HEXCodes.LAVENDER_GRAY, Layer.Background),
        'LAWN_GREEN': Color.hex_to_ansi(HEXCodes.LAWN_GREEN, Layer.Background),
        'LEMON': Color.hex_to_ansi(HEXCodes.LEMON, Layer.Background),
        'LEMON_CHIFFON': Color.hex_to_ansi(HEXCodes.LEMON_CHIFFON, Layer.Background),
        'LEMON_CURRY': Color.hex_to_ansi(HEXCodes.LEMON_CURRY, Layer.Background),
        'LEMON_GLACIER': Color.hex_to_ansi(HEXCodes.LEMON_GLACIER, Layer.Background),
        'LEMON_MERINGUE': Color.hex_to_ansi(HEXCodes.LEMON_MERINGUE, Layer.Background),
        'LEMON_YELLOW': Color.hex_to_ansi(HEXCodes.LEMON_YELLOW, Layer.Background),
        'LEMON_YELLOW_CRAYOLA': Color.hex_to_ansi(HEXCodes.LEMON_YELLOW_CRAYOLA, Layer.Background),
        'LIBERTY': Color.hex_to_ansi(HEXCodes.LIBERTY, Layer.Background),
        'LIGHT_BLUE': Color.hex_to_ansi(HEXCodes.LIGHT_BLUE, Layer.Background),
        'LIGHT_CORAL': Color.hex_to_ansi(HEXCodes.LIGHT_CORAL, Layer.Background),
        'LIGHT_CORNFLOWER_BLUE': Color.hex_to_ansi(HEXCodes.LIGHT_CORNFLOWER_BLUE, Layer.Background),
        'LIGHT_CYAN': Color.hex_to_ansi(HEXCodes.LIGHT_CYAN, Layer.Background),
        'LIGHT_FRENCH_BEIGE': Color.hex_to_ansi(HEXCodes.LIGHT_FRENCH_BEIGE, Layer.Background),
        'LIGHT_GOLDENROD_YELLOW': Color.hex_to_ansi(HEXCodes.LIGHT_GOLDENROD_YELLOW, Layer.Background),
        'LIGHT_GRAY': Color.hex_to_ansi(HEXCodes.LIGHT_GRAY, Layer.Background),
        'LIGHT_GREEN': Color.hex_to_ansi(HEXCodes.LIGHT_GREEN, Layer.Background),
        'LIGHT_ORANGE': Color.hex_to_ansi(HEXCodes.LIGHT_ORANGE, Layer.Background),
        'LIGHT_PERIWINKLE': Color.hex_to_ansi(HEXCodes.LIGHT_PERIWINKLE, Layer.Background),
        'LIGHT_PINK': Color.hex_to_ansi(HEXCodes.LIGHT_PINK, Layer.Background),
        'LIGHT_SALMON': Color.hex_to_ansi(HEXCodes.LIGHT_SALMON, Layer.Background),
        'LIGHT_SEA_GREEN': Color.hex_to_ansi(HEXCodes.LIGHT_SEA_GREEN, Layer.Background),
        'LIGHT_SKY_BLUE': Color.hex_to_ansi(HEXCodes.LIGHT_SKY_BLUE, Layer.Background),
        'LIGHT_SLATE_GRAY': Color.hex_to_ansi(HEXCodes.LIGHT_SLATE_GRAY, Layer.Background),
        'LIGHT_STEEL_BLUE': Color.hex_to_ansi(HEXCodes.LIGHT_STEEL_BLUE, Layer.Background),
        'LIGHT_YELLOW': Color.hex_to_ansi(HEXCodes.LIGHT_YELLOW, Layer.Background),
        'LILAC': Color.hex_to_ansi(HEXCodes.LILAC, Layer.Background),
        'LILAC_LUSTER': Color.hex_to_ansi(HEXCodes.LILAC_LUSTER, Layer.Background),
        'LIME_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.LIME_COLOR_WHEEL, Layer.Background),
        'LIME_WEB_X11_GREEN': Color.hex_to_ansi(HEXCodes.LIME_WEB_X11_GREEN, Layer.Background),
        'LIME_GREEN': Color.hex_to_ansi(HEXCodes.LIME_GREEN, Layer.Background),
        'LINCOLN_GREEN': Color.hex_to_ansi(HEXCodes.LINCOLN_GREEN, Layer.Background),
        'LINEN': Color.hex_to_ansi(HEXCodes.LINEN, Layer.Background),
        'LION': Color.hex_to_ansi(HEXCodes.LION, Layer.Background),
        'LISERAN_PURPLE': Color.hex_to_ansi(HEXCodes.LISERAN_PURPLE, Layer.Background),
        'LITTLE_BOY_BLUE': Color.hex_to_ansi(HEXCodes.LITTLE_BOY_BLUE, Layer.Background),
        'LIVER': Color.hex_to_ansi(HEXCodes.LIVER, Layer.Background),
        'LIVER_DOGS': Color.hex_to_ansi(HEXCodes.LIVER_DOGS, Layer.Background),
        'LIVER_ORGAN': Color.hex_to_ansi(HEXCodes.LIVER_ORGAN, Layer.Background),
        'LIVER_CHESTNUT': Color.hex_to_ansi(HEXCodes.LIVER_CHESTNUT, Layer.Background),
        'LIVID': Color.hex_to_ansi(HEXCodes.LIVID, Layer.Background),
        'MACARONI_AND_CHEESE': Color.hex_to_ansi(HEXCodes.MACARONI_AND_CHEESE, Layer.Background),
        'MADDER_LAKE': Color.hex_to_ansi(HEXCodes.MADDER_LAKE, Layer.Background),
        'MAGENTA_CRAYOLA': Color.hex_to_ansi(HEXCodes.MAGENTA_CRAYOLA, Layer.Background),
        'MAGENTA_DYE': Color.hex_to_ansi(HEXCodes.MAGENTA_DYE, Layer.Background),
        'MAGENTA_PANTONE': Color.hex_to_ansi(HEXCodes.MAGENTA_PANTONE, Layer.Background),
        'MAGENTA_PROCESS': Color.hex_to_ansi(HEXCodes.MAGENTA_PROCESS, Layer.Background),
        'MAGENTA_HAZE': Color.hex_to_ansi(HEXCodes.MAGENTA_HAZE, Layer.Background),
        'MAGIC_MINT': Color.hex_to_ansi(HEXCodes.MAGIC_MINT, Layer.Background),
        'MAGNOLIA': Color.hex_to_ansi(HEXCodes.MAGNOLIA, Layer.Background),
        'MAHOGANY': Color.hex_to_ansi(HEXCodes.MAHOGANY, Layer.Background),
        'MAIZE': Color.hex_to_ansi(HEXCodes.MAIZE, Layer.Background),
        'MAIZE_CRAYOLA': Color.hex_to_ansi(HEXCodes.MAIZE_CRAYOLA, Layer.Background),
        'MAJORELLE_BLUE': Color.hex_to_ansi(HEXCodes.MAJORELLE_BLUE, Layer.Background),
        'MALACHITE': Color.hex_to_ansi(HEXCodes.MALACHITE, Layer.Background),
        'MANATEE': Color.hex_to_ansi(HEXCodes.MANATEE, Layer.Background),
        'MANDARIN': Color.hex_to_ansi(HEXCodes.MANDARIN, Layer.Background),
        'MANGO': Color.hex_to_ansi(HEXCodes.MANGO, Layer.Background),
        'MANGO_TANGO': Color.hex_to_ansi(HEXCodes.MANGO_TANGO, Layer.Background),
        'MANTIS': Color.hex_to_ansi(HEXCodes.MANTIS, Layer.Background),
        'MARDI_GRAS': Color.hex_to_ansi(HEXCodes.MARDI_GRAS, Layer.Background),
        'MARIGOLD': Color.hex_to_ansi(HEXCodes.MARIGOLD, Layer.Background),
        'MAROON_CRAYOLA': Color.hex_to_ansi(HEXCodes.MAROON_CRAYOLA, Layer.Background),
        'MAROON_WEB': Color.hex_to_ansi(HEXCodes.MAROON_WEB, Layer.Background),
        'MAROON_X11': Color.hex_to_ansi(HEXCodes.MAROON_X11, Layer.Background),
        'MAUVE': Color.hex_to_ansi(HEXCodes.MAUVE, Layer.Background),
        'MAUVE_TAUPE': Color.hex_to_ansi(HEXCodes.MAUVE_TAUPE, Layer.Background),
        'MAUVELOUS': Color.hex_to_ansi(HEXCodes.MAUVELOUS, Layer.Background),
        'MAXIMUM_BLUE': Color.hex_to_ansi(HEXCodes.MAXIMUM_BLUE, Layer.Background),
        'MAXIMUM_BLUE_GREEN': Color.hex_to_ansi(HEXCodes.MAXIMUM_BLUE_GREEN, Layer.Background),
        'MAXIMUM_BLUE_PURPLE': Color.hex_to_ansi(HEXCodes.MAXIMUM_BLUE_PURPLE, Layer.Background),
        'MAXIMUM_GREEN': Color.hex_to_ansi(HEXCodes.MAXIMUM_GREEN, Layer.Background),
        'MAXIMUM_GREEN_YELLOW': Color.hex_to_ansi(HEXCodes.MAXIMUM_GREEN_YELLOW, Layer.Background),
        'MAXIMUM_PURPLE': Color.hex_to_ansi(HEXCodes.MAXIMUM_PURPLE, Layer.Background),
        'MAXIMUM_RED': Color.hex_to_ansi(HEXCodes.MAXIMUM_RED, Layer.Background),
        'MAXIMUM_RED_PURPLE': Color.hex_to_ansi(HEXCodes.MAXIMUM_RED_PURPLE, Layer.Background),
        'MAXIMUM_YELLOW': Color.hex_to_ansi(HEXCodes.MAXIMUM_YELLOW, Layer.Background),
        'MAXIMUM_YELLOW_RED': Color.hex_to_ansi(HEXCodes.MAXIMUM_YELLOW_RED, Layer.Background),
        'MAY_GREEN': Color.hex_to_ansi(HEXCodes.MAY_GREEN, Layer.Background),
        'MAYA_BLUE': Color.hex_to_ansi(HEXCodes.MAYA_BLUE, Layer.Background),
        'MEDIUM_AQUAMARINE': Color.hex_to_ansi(HEXCodes.MEDIUM_AQUAMARINE, Layer.Background),
        'MEDIUM_BLUE': Color.hex_to_ansi(HEXCodes.MEDIUM_BLUE, Layer.Background),
        'MEDIUM_CANDY_APPLE_RED': Color.hex_to_ansi(HEXCodes.MEDIUM_CANDY_APPLE_RED, Layer.Background),
        'MEDIUM_CARMINE': Color.hex_to_ansi(HEXCodes.MEDIUM_CARMINE, Layer.Background),
        'MEDIUM_CHAMPAGNE': Color.hex_to_ansi(HEXCodes.MEDIUM_CHAMPAGNE, Layer.Background),
        'MEDIUM_ORCHID': Color.hex_to_ansi(HEXCodes.MEDIUM_ORCHID, Layer.Background),
        'MEDIUM_PURPLE': Color.hex_to_ansi(HEXCodes.MEDIUM_PURPLE, Layer.Background),
        'MEDIUM_SEA_GREEN': Color.hex_to_ansi(HEXCodes.MEDIUM_SEA_GREEN, Layer.Background),
        'MEDIUM_SLATE_BLUE': Color.hex_to_ansi(HEXCodes.MEDIUM_SLATE_BLUE, Layer.Background),
        'MEDIUM_SPRING_GREEN': Color.hex_to_ansi(HEXCodes.MEDIUM_SPRING_GREEN, Layer.Background),
        'MEDIUM_TURQUOISE': Color.hex_to_ansi(HEXCodes.MEDIUM_TURQUOISE, Layer.Background),
        'MEDIUM_VIOLET_RED': Color.hex_to_ansi(HEXCodes.MEDIUM_VIOLET_RED, Layer.Background),
        'MELLOW_APRICOT': Color.hex_to_ansi(HEXCodes.MELLOW_APRICOT, Layer.Background),
        'MELLOW_YELLOW': Color.hex_to_ansi(HEXCodes.MELLOW_YELLOW, Layer.Background),
        'MELON': Color.hex_to_ansi(HEXCodes.MELON, Layer.Background),
        'METALLIC_GOLD': Color.hex_to_ansi(HEXCodes.METALLIC_GOLD, Layer.Background),
        'METALLIC_SEAWEED': Color.hex_to_ansi(HEXCodes.METALLIC_SEAWEED, Layer.Background),
        'METALLIC_SUNBURST': Color.hex_to_ansi(HEXCodes.METALLIC_SUNBURST, Layer.Background),
        'MEXICAN_PINK': Color.hex_to_ansi(HEXCodes.MEXICAN_PINK, Layer.Background),
        'MIDDLE_BLUE': Color.hex_to_ansi(HEXCodes.MIDDLE_BLUE, Layer.Background),
        'MIDDLE_BLUE_GREEN': Color.hex_to_ansi(HEXCodes.MIDDLE_BLUE_GREEN, Layer.Background),
        'MIDDLE_BLUE_PURPLE': Color.hex_to_ansi(HEXCodes.MIDDLE_BLUE_PURPLE, Layer.Background),
        'MIDDLE_GREY': Color.hex_to_ansi(HEXCodes.MIDDLE_GREY, Layer.Background),
        'MIDDLE_GREEN': Color.hex_to_ansi(HEXCodes.MIDDLE_GREEN, Layer.Background),
        'MIDDLE_GREEN_YELLOW': Color.hex_to_ansi(HEXCodes.MIDDLE_GREEN_YELLOW, Layer.Background),
        'MIDDLE_PURPLE': Color.hex_to_ansi(HEXCodes.MIDDLE_PURPLE, Layer.Background),
        'MIDDLE_RED': Color.hex_to_ansi(HEXCodes.MIDDLE_RED, Layer.Background),
        'MIDDLE_RED_PURPLE': Color.hex_to_ansi(HEXCodes.MIDDLE_RED_PURPLE, Layer.Background),
        'MIDDLE_YELLOW': Color.hex_to_ansi(HEXCodes.MIDDLE_YELLOW, Layer.Background),
        'MIDDLE_YELLOW_RED': Color.hex_to_ansi(HEXCodes.MIDDLE_YELLOW_RED, Layer.Background),
        'MIDNIGHT': Color.hex_to_ansi(HEXCodes.MIDNIGHT, Layer.Background),
        'MIDNIGHT_BLUE': Color.hex_to_ansi(HEXCodes.MIDNIGHT_BLUE, Layer.Background),
        'MIDNIGHT_GREEN_EAGLE_GREEN': Color.hex_to_ansi(HEXCodes.MIDNIGHT_GREEN_EAGLE_GREEN, Layer.Background),
        'MIKADO_YELLOW': Color.hex_to_ansi(HEXCodes.MIKADO_YELLOW, Layer.Background),
        'MIMI_PINK': Color.hex_to_ansi(HEXCodes.MIMI_PINK, Layer.Background),
        'MINDARO': Color.hex_to_ansi(HEXCodes.MINDARO, Layer.Background),
        'MING': Color.hex_to_ansi(HEXCodes.MING, Layer.Background),
        'MINION_YELLOW': Color.hex_to_ansi(HEXCodes.MINION_YELLOW, Layer.Background),
        'MINT': Color.hex_to_ansi(HEXCodes.MINT, Layer.Background),
        'MINT_CREAM': Color.hex_to_ansi(HEXCodes.MINT_CREAM, Layer.Background),
        'MINT_GREEN': Color.hex_to_ansi(HEXCodes.MINT_GREEN, Layer.Background),
        'MISTY_MOSS': Color.hex_to_ansi(HEXCodes.MISTY_MOSS, Layer.Background),
        'MISTY_ROSE': Color.hex_to_ansi(HEXCodes.MISTY_ROSE, Layer.Background),
        'MODE_BEIGE': Color.hex_to_ansi(HEXCodes.MODE_BEIGE, Layer.Background),
        'MONA_LISA': Color.hex_to_ansi(HEXCodes.MONA_LISA, Layer.Background),
        'MORNING_BLUE': Color.hex_to_ansi(HEXCodes.MORNING_BLUE, Layer.Background),
        'MOSS_GREEN': Color.hex_to_ansi(HEXCodes.MOSS_GREEN, Layer.Background),
        'MOUNTAIN_MEADOW': Color.hex_to_ansi(HEXCodes.MOUNTAIN_MEADOW, Layer.Background),
        'MOUNTBATTEN_PINK': Color.hex_to_ansi(HEXCodes.MOUNTBATTEN_PINK, Layer.Background),
        'MSU_GREEN': Color.hex_to_ansi(HEXCodes.MSU_GREEN, Layer.Background),
        'MULBERRY': Color.hex_to_ansi(HEXCodes.MULBERRY, Layer.Background),
        'MULBERRY_CRAYOLA': Color.hex_to_ansi(HEXCodes.MULBERRY_CRAYOLA, Layer.Background),
        'MUSTARD': Color.hex_to_ansi(HEXCodes.MUSTARD, Layer.Background),
        'MYRTLE_GREEN': Color.hex_to_ansi(HEXCodes.MYRTLE_GREEN, Layer.Background),
        'MYSTIC': Color.hex_to_ansi(HEXCodes.MYSTIC, Layer.Background),
        'MYSTIC_MAROON': Color.hex_to_ansi(HEXCodes.MYSTIC_MAROON, Layer.Background),
        'NADESHIKO_PINK': Color.hex_to_ansi(HEXCodes.NADESHIKO_PINK, Layer.Background),
        'NAPLES_YELLOW': Color.hex_to_ansi(HEXCodes.NAPLES_YELLOW, Layer.Background),
        'NAVAJO_WHITE': Color.hex_to_ansi(HEXCodes.NAVAJO_WHITE, Layer.Background),
        'NAVY_BLUE': Color.hex_to_ansi(HEXCodes.NAVY_BLUE, Layer.Background),
        'NAVY_BLUE_CRAYOLA': Color.hex_to_ansi(HEXCodes.NAVY_BLUE_CRAYOLA, Layer.Background),
        'NEON_BLUE': Color.hex_to_ansi(HEXCodes.NEON_BLUE, Layer.Background),
        'NEON_GREEN': Color.hex_to_ansi(HEXCodes.NEON_GREEN, Layer.Background),
        'NEON_FUCHSIA': Color.hex_to_ansi(HEXCodes.NEON_FUCHSIA, Layer.Background),
        'NEW_CAR': Color.hex_to_ansi(HEXCodes.NEW_CAR, Layer.Background),
        'NEW_YORK_PINK': Color.hex_to_ansi(HEXCodes.NEW_YORK_PINK, Layer.Background),
        'NICKEL': Color.hex_to_ansi(HEXCodes.NICKEL, Layer.Background),
        'NON_PHOTO_BLUE': Color.hex_to_ansi(HEXCodes.NON_PHOTO_BLUE, Layer.Background),
        'NYANZA': Color.hex_to_ansi(HEXCodes.NYANZA, Layer.Background),
        'OCHRE': Color.hex_to_ansi(HEXCodes.OCHRE, Layer.Background),
        'OLD_BURGUNDY': Color.hex_to_ansi(HEXCodes.OLD_BURGUNDY, Layer.Background),
        'OLD_GOLD': Color.hex_to_ansi(HEXCodes.OLD_GOLD, Layer.Background),
        'OLD_LACE': Color.hex_to_ansi(HEXCodes.OLD_LACE, Layer.Background),
        'OLD_LAVENDER': Color.hex_to_ansi(HEXCodes.OLD_LAVENDER, Layer.Background),
        'OLD_MAUVE': Color.hex_to_ansi(HEXCodes.OLD_MAUVE, Layer.Background),
        'OLD_ROSE': Color.hex_to_ansi(HEXCodes.OLD_ROSE, Layer.Background),
        'OLD_SILVER': Color.hex_to_ansi(HEXCodes.OLD_SILVER, Layer.Background),
        'OLIVE': Color.hex_to_ansi(HEXCodes.OLIVE, Layer.Background),
        'OLIVE_DRAB_3': Color.hex_to_ansi(HEXCodes.OLIVE_DRAB_3, Layer.Background),
        'OLIVE_DRAB_7': Color.hex_to_ansi(HEXCodes.OLIVE_DRAB_7, Layer.Background),
        'OLIVE_GREEN': Color.hex_to_ansi(HEXCodes.OLIVE_GREEN, Layer.Background),
        'OLIVINE': Color.hex_to_ansi(HEXCodes.OLIVINE, Layer.Background),
        'ONYX': Color.hex_to_ansi(HEXCodes.ONYX, Layer.Background),
        'OPAL': Color.hex_to_ansi(HEXCodes.OPAL, Layer.Background),
        'OPERA_MAUVE': Color.hex_to_ansi(HEXCodes.OPERA_MAUVE, Layer.Background),
        'ORANGE': Color.hex_to_ansi(HEXCodes.ORANGE, Layer.Background),
        'ORANGE_CRAYOLA': Color.hex_to_ansi(HEXCodes.ORANGE_CRAYOLA, Layer.Background),
        'ORANGE_PANTONE': Color.hex_to_ansi(HEXCodes.ORANGE_PANTONE, Layer.Background),
        'ORANGE_WEB': Color.hex_to_ansi(HEXCodes.ORANGE_WEB, Layer.Background),
        'ORANGE_PEEL': Color.hex_to_ansi(HEXCodes.ORANGE_PEEL, Layer.Background),
        'ORANGE_RED': Color.hex_to_ansi(HEXCodes.ORANGE_RED, Layer.Background),
        'ORANGE_RED_CRAYOLA': Color.hex_to_ansi(HEXCodes.ORANGE_RED_CRAYOLA, Layer.Background),
        'ORANGE_SODA': Color.hex_to_ansi(HEXCodes.ORANGE_SODA, Layer.Background),
        'ORANGE_YELLOW': Color.hex_to_ansi(HEXCodes.ORANGE_YELLOW, Layer.Background),
        'ORANGE_YELLOW_CRAYOLA': Color.hex_to_ansi(HEXCodes.ORANGE_YELLOW_CRAYOLA, Layer.Background),
        'ORCHID': Color.hex_to_ansi(HEXCodes.ORCHID, Layer.Background),
        'ORCHID_PINK': Color.hex_to_ansi(HEXCodes.ORCHID_PINK, Layer.Background),
        'ORCHID_CRAYOLA': Color.hex_to_ansi(HEXCodes.ORCHID_CRAYOLA, Layer.Background),
        'OUTER_SPACE_CRAYOLA': Color.hex_to_ansi(HEXCodes.OUTER_SPACE_CRAYOLA, Layer.Background),
        'OUTRAGEOUS_ORANGE': Color.hex_to_ansi(HEXCodes.OUTRAGEOUS_ORANGE, Layer.Background),
        'OXBLOOD': Color.hex_to_ansi(HEXCodes.OXBLOOD, Layer.Background),
        'OXFORD_BLUE': Color.hex_to_ansi(HEXCodes.OXFORD_BLUE, Layer.Background),
        'OU_CRIMSON_RED': Color.hex_to_ansi(HEXCodes.OU_CRIMSON_RED, Layer.Background),
        'PACIFIC_BLUE': Color.hex_to_ansi(HEXCodes.PACIFIC_BLUE, Layer.Background),
        'PAKISTAN_GREEN': Color.hex_to_ansi(HEXCodes.PAKISTAN_GREEN, Layer.Background),
        'PALATINATE_PURPLE': Color.hex_to_ansi(HEXCodes.PALATINATE_PURPLE, Layer.Background),
        'PALE_AQUA': Color.hex_to_ansi(HEXCodes.PALE_AQUA, Layer.Background),
        'PALE_CERULEAN': Color.hex_to_ansi(HEXCodes.PALE_CERULEAN, Layer.Background),
        'PALE_DOGWOOD': Color.hex_to_ansi(HEXCodes.PALE_DOGWOOD, Layer.Background),
        'PALE_PINK': Color.hex_to_ansi(HEXCodes.PALE_PINK, Layer.Background),
        'PALE_PURPLE_PANTONE': Color.hex_to_ansi(HEXCodes.PALE_PURPLE_PANTONE, Layer.Background),
        'PALE_SPRING_BUD': Color.hex_to_ansi(HEXCodes.PALE_SPRING_BUD, Layer.Background),
        'PANSY_PURPLE': Color.hex_to_ansi(HEXCodes.PANSY_PURPLE, Layer.Background),
        'PAOLO_VERONESE_GREEN': Color.hex_to_ansi(HEXCodes.PAOLO_VERONESE_GREEN, Layer.Background),
        'PAPAYA_WHIP': Color.hex_to_ansi(HEXCodes.PAPAYA_WHIP, Layer.Background),
        'PARADISE_PINK': Color.hex_to_ansi(HEXCodes.PARADISE_PINK, Layer.Background),
        'PARCHMENT': Color.hex_to_ansi(HEXCodes.PARCHMENT, Layer.Background),
        'PARIS_GREEN': Color.hex_to_ansi(HEXCodes.PARIS_GREEN, Layer.Background),
        'PASTEL_PINK': Color.hex_to_ansi(HEXCodes.PASTEL_PINK, Layer.Background),
        'PATRIARCH': Color.hex_to_ansi(HEXCodes.PATRIARCH, Layer.Background),
        'PAUA': Color.hex_to_ansi(HEXCodes.PAUA, Layer.Background),
        'PAYNE_S_GREY': Color.hex_to_ansi(HEXCodes.PAYNE_S_GREY, Layer.Background),
        'PEACH': Color.hex_to_ansi(HEXCodes.PEACH, Layer.Background),
        'PEACH_CRAYOLA': Color.hex_to_ansi(HEXCodes.PEACH_CRAYOLA, Layer.Background),
        'PEACH_PUFF': Color.hex_to_ansi(HEXCodes.PEACH_PUFF, Layer.Background),
        'PEAR': Color.hex_to_ansi(HEXCodes.PEAR, Layer.Background),
        'PEARLY_PURPLE': Color.hex_to_ansi(HEXCodes.PEARLY_PURPLE, Layer.Background),
        'PERIWINKLE': Color.hex_to_ansi(HEXCodes.PERIWINKLE, Layer.Background),
        'PERIWINKLE_CRAYOLA': Color.hex_to_ansi(HEXCodes.PERIWINKLE_CRAYOLA, Layer.Background),
        'PERMANENT_GERANIUM_LAKE': Color.hex_to_ansi(HEXCodes.PERMANENT_GERANIUM_LAKE, Layer.Background),
        'PERSIAN_BLUE': Color.hex_to_ansi(HEXCodes.PERSIAN_BLUE, Layer.Background),
        'PERSIAN_GREEN': Color.hex_to_ansi(HEXCodes.PERSIAN_GREEN, Layer.Background),
        'PERSIAN_INDIGO': Color.hex_to_ansi(HEXCodes.PERSIAN_INDIGO, Layer.Background),
        'PERSIAN_ORANGE': Color.hex_to_ansi(HEXCodes.PERSIAN_ORANGE, Layer.Background),
        'PERSIAN_PINK': Color.hex_to_ansi(HEXCodes.PERSIAN_PINK, Layer.Background),
        'PERSIAN_PLUM': Color.hex_to_ansi(HEXCodes.PERSIAN_PLUM, Layer.Background),
        'PERSIAN_RED': Color.hex_to_ansi(HEXCodes.PERSIAN_RED, Layer.Background),
        'PERSIAN_ROSE': Color.hex_to_ansi(HEXCodes.PERSIAN_ROSE, Layer.Background),
        'PERSIMMON': Color.hex_to_ansi(HEXCodes.PERSIMMON, Layer.Background),
        'PEWTER_BLUE': Color.hex_to_ansi(HEXCodes.PEWTER_BLUE, Layer.Background),
        'PHLOX': Color.hex_to_ansi(HEXCodes.PHLOX, Layer.Background),
        'PHTHALO_BLUE': Color.hex_to_ansi(HEXCodes.PHTHALO_BLUE, Layer.Background),
        'PHTHALO_GREEN': Color.hex_to_ansi(HEXCodes.PHTHALO_GREEN, Layer.Background),
        'PICOTEE_BLUE': Color.hex_to_ansi(HEXCodes.PICOTEE_BLUE, Layer.Background),
        'PICTORIAL_CARMINE': Color.hex_to_ansi(HEXCodes.PICTORIAL_CARMINE, Layer.Background),
        'PIGGY_PINK': Color.hex_to_ansi(HEXCodes.PIGGY_PINK, Layer.Background),
        'PINE_GREEN': Color.hex_to_ansi(HEXCodes.PINE_GREEN, Layer.Background),
        'PINK': Color.hex_to_ansi(HEXCodes.PINK, Layer.Background),
        'PINK_PANTONE': Color.hex_to_ansi(HEXCodes.PINK_PANTONE, Layer.Background),
        'PINK_LACE': Color.hex_to_ansi(HEXCodes.PINK_LACE, Layer.Background),
        'PINK_LAVENDER': Color.hex_to_ansi(HEXCodes.PINK_LAVENDER, Layer.Background),
        'PINK_SHERBET': Color.hex_to_ansi(HEXCodes.PINK_SHERBET, Layer.Background),
        'PISTACHIO': Color.hex_to_ansi(HEXCodes.PISTACHIO, Layer.Background),
        'PLATINUM': Color.hex_to_ansi(HEXCodes.PLATINUM, Layer.Background),
        'PLUM': Color.hex_to_ansi(HEXCodes.PLUM, Layer.Background),
        'PLUM_WEB': Color.hex_to_ansi(HEXCodes.PLUM_WEB, Layer.Background),
        'PLUMP_PURPLE': Color.hex_to_ansi(HEXCodes.PLUMP_PURPLE, Layer.Background),
        'POLISHED_PINE': Color.hex_to_ansi(HEXCodes.POLISHED_PINE, Layer.Background),
        'POMP_AND_POWER': Color.hex_to_ansi(HEXCodes.POMP_AND_POWER, Layer.Background),
        'POPSTAR': Color.hex_to_ansi(HEXCodes.POPSTAR, Layer.Background),
        'PORTLAND_ORANGE': Color.hex_to_ansi(HEXCodes.PORTLAND_ORANGE, Layer.Background),
        'POWDER_BLUE': Color.hex_to_ansi(HEXCodes.POWDER_BLUE, Layer.Background),
        'PRAIRIE_GOLD': Color.hex_to_ansi(HEXCodes.PRAIRIE_GOLD, Layer.Background),
        'PRINCETON_ORANGE': Color.hex_to_ansi(HEXCodes.PRINCETON_ORANGE, Layer.Background),
        'PRUNE': Color.hex_to_ansi(HEXCodes.PRUNE, Layer.Background),
        'PRUSSIAN_BLUE': Color.hex_to_ansi(HEXCodes.PRUSSIAN_BLUE, Layer.Background),
        'PSYCHEDELIC_PURPLE': Color.hex_to_ansi(HEXCodes.PSYCHEDELIC_PURPLE, Layer.Background),
        'PUCE': Color.hex_to_ansi(HEXCodes.PUCE, Layer.Background),
        'PULLMAN_BROWN_UPS_BROWN': Color.hex_to_ansi(HEXCodes.PULLMAN_BROWN_UPS_BROWN, Layer.Background),
        'PUMPKIN': Color.hex_to_ansi(HEXCodes.PUMPKIN, Layer.Background),
        'PURPLE': Color.hex_to_ansi(HEXCodes.PURPLE, Layer.Background),
        'PURPLE_WEB': Color.hex_to_ansi(HEXCodes.PURPLE_WEB, Layer.Background),
        'PURPLE_MUNSELL': Color.hex_to_ansi(HEXCodes.PURPLE_MUNSELL, Layer.Background),
        'PURPLE_X11': Color.hex_to_ansi(HEXCodes.PURPLE_X11, Layer.Background),
        'PURPLE_MOUNTAIN_MAJESTY': Color.hex_to_ansi(HEXCodes.PURPLE_MOUNTAIN_MAJESTY, Layer.Background),
        'PURPLE_NAVY': Color.hex_to_ansi(HEXCodes.PURPLE_NAVY, Layer.Background),
        'PURPLE_PIZZAZZ': Color.hex_to_ansi(HEXCodes.PURPLE_PIZZAZZ, Layer.Background),
        'PURPLE_PLUM': Color.hex_to_ansi(HEXCodes.PURPLE_PLUM, Layer.Background),
        'PURPUREUS': Color.hex_to_ansi(HEXCodes.PURPUREUS, Layer.Background),
        'QUEEN_BLUE': Color.hex_to_ansi(HEXCodes.QUEEN_BLUE, Layer.Background),
        'QUEEN_PINK': Color.hex_to_ansi(HEXCodes.QUEEN_PINK, Layer.Background),
        'QUICK_SILVER': Color.hex_to_ansi(HEXCodes.QUICK_SILVER, Layer.Background),
        'QUINACRIDONE_MAGENTA': Color.hex_to_ansi(HEXCodes.QUINACRIDONE_MAGENTA, Layer.Background),
        'RADICAL_RED': Color.hex_to_ansi(HEXCodes.RADICAL_RED, Layer.Background),
        'RAISIN_BLACK': Color.hex_to_ansi(HEXCodes.RAISIN_BLACK, Layer.Background),
        'RAJAH': Color.hex_to_ansi(HEXCodes.RAJAH, Layer.Background),
        'RASPBERRY': Color.hex_to_ansi(HEXCodes.RASPBERRY, Layer.Background),
        'RASPBERRY_GLACE': Color.hex_to_ansi(HEXCodes.RASPBERRY_GLACE, Layer.Background),
        'RASPBERRY_ROSE': Color.hex_to_ansi(HEXCodes.RASPBERRY_ROSE, Layer.Background),
        'RAW_SIENNA': Color.hex_to_ansi(HEXCodes.RAW_SIENNA, Layer.Background),
        'RAW_UMBER': Color.hex_to_ansi(HEXCodes.RAW_UMBER, Layer.Background),
        'RAZZLE_DAZZLE_ROSE': Color.hex_to_ansi(HEXCodes.RAZZLE_DAZZLE_ROSE, Layer.Background),
        'RAZZMATAZZ': Color.hex_to_ansi(HEXCodes.RAZZMATAZZ, Layer.Background),
        'RAZZMIC_BERRY': Color.hex_to_ansi(HEXCodes.RAZZMIC_BERRY, Layer.Background),
        'REBECCA_PURPLE': Color.hex_to_ansi(HEXCodes.REBECCA_PURPLE, Layer.Background),
        'RED_CRAYOLA': Color.hex_to_ansi(HEXCodes.RED_CRAYOLA, Layer.Background),
        'RED_MUNSELL': Color.hex_to_ansi(HEXCodes.RED_MUNSELL, Layer.Background),
        'RED_NCS': Color.hex_to_ansi(HEXCodes.RED_NCS, Layer.Background),
        'RED_PANTONE': Color.hex_to_ansi(HEXCodes.RED_PANTONE, Layer.Background),
        'RED_PIGMENT': Color.hex_to_ansi(HEXCodes.RED_PIGMENT, Layer.Background),
        'RED_RYB': Color.hex_to_ansi(HEXCodes.RED_RYB, Layer.Background),
        'RED_ORANGE': Color.hex_to_ansi(HEXCodes.RED_ORANGE, Layer.Background),
        'RED_ORANGE_CRAYOLA': Color.hex_to_ansi(HEXCodes.RED_ORANGE_CRAYOLA, Layer.Background),
        'RED_ORANGE_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.RED_ORANGE_COLOR_WHEEL, Layer.Background),
        'RED_PURPLE': Color.hex_to_ansi(HEXCodes.RED_PURPLE, Layer.Background),
        'RED_SALSA': Color.hex_to_ansi(HEXCodes.RED_SALSA, Layer.Background),
        'RED_VIOLET': Color.hex_to_ansi(HEXCodes.RED_VIOLET, Layer.Background),
        'RED_VIOLET_CRAYOLA': Color.hex_to_ansi(HEXCodes.RED_VIOLET_CRAYOLA, Layer.Background),
        'RED_VIOLET_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.RED_VIOLET_COLOR_WHEEL, Layer.Background),
        'REDWOOD': Color.hex_to_ansi(HEXCodes.REDWOOD, Layer.Background),
        'RESOLUTION_BLUE': Color.hex_to_ansi(HEXCodes.RESOLUTION_BLUE, Layer.Background),
        'RHYTHM': Color.hex_to_ansi(HEXCodes.RHYTHM, Layer.Background),
        'RICH_BLACK': Color.hex_to_ansi(HEXCodes.RICH_BLACK, Layer.Background),
        'RICH_BLACK_FOGRA29': Color.hex_to_ansi(HEXCodes.RICH_BLACK_FOGRA29, Layer.Background),
        'RICH_BLACK_FOGRA39': Color.hex_to_ansi(HEXCodes.RICH_BLACK_FOGRA39, Layer.Background),
        'RIFLE_GREEN': Color.hex_to_ansi(HEXCodes.RIFLE_GREEN, Layer.Background),
        'ROBIN_EGG_BLUE': Color.hex_to_ansi(HEXCodes.ROBIN_EGG_BLUE, Layer.Background),
        'ROCKET_METALLIC': Color.hex_to_ansi(HEXCodes.ROCKET_METALLIC, Layer.Background),
        'ROJO_SPANISH_RED': Color.hex_to_ansi(HEXCodes.ROJO_SPANISH_RED, Layer.Background),
        'ROMAN_SILVER': Color.hex_to_ansi(HEXCodes.ROMAN_SILVER, Layer.Background),
        'ROSE': Color.hex_to_ansi(HEXCodes.ROSE, Layer.Background),
        'ROSE_BONBON': Color.hex_to_ansi(HEXCodes.ROSE_BONBON, Layer.Background),
        'ROSE_DUST': Color.hex_to_ansi(HEXCodes.ROSE_DUST, Layer.Background),
        'ROSE_EBONY': Color.hex_to_ansi(HEXCodes.ROSE_EBONY, Layer.Background),
        'ROSE_MADDER': Color.hex_to_ansi(HEXCodes.ROSE_MADDER, Layer.Background),
        'ROSE_PINK': Color.hex_to_ansi(HEXCodes.ROSE_PINK, Layer.Background),
        'ROSE_POMPADOUR': Color.hex_to_ansi(HEXCodes.ROSE_POMPADOUR, Layer.Background),
        'ROSE_RED': Color.hex_to_ansi(HEXCodes.ROSE_RED, Layer.Background),
        'ROSE_TAUPE': Color.hex_to_ansi(HEXCodes.ROSE_TAUPE, Layer.Background),
        'ROSE_VALE': Color.hex_to_ansi(HEXCodes.ROSE_VALE, Layer.Background),
        'ROSEWOOD': Color.hex_to_ansi(HEXCodes.ROSEWOOD, Layer.Background),
        'ROSSO_CORSA': Color.hex_to_ansi(HEXCodes.ROSSO_CORSA, Layer.Background),
        'ROSY_BROWN': Color.hex_to_ansi(HEXCodes.ROSY_BROWN, Layer.Background),
        'ROYAL_BLUE_DARK': Color.hex_to_ansi(HEXCodes.ROYAL_BLUE_DARK, Layer.Background),
        'ROYAL_BLUE_LIGHT': Color.hex_to_ansi(HEXCodes.ROYAL_BLUE_LIGHT, Layer.Background),
        'ROYAL_PURPLE': Color.hex_to_ansi(HEXCodes.ROYAL_PURPLE, Layer.Background),
        'ROYAL_YELLOW': Color.hex_to_ansi(HEXCodes.ROYAL_YELLOW, Layer.Background),
        'RUBER': Color.hex_to_ansi(HEXCodes.RUBER, Layer.Background),
        'RUBINE_RED': Color.hex_to_ansi(HEXCodes.RUBINE_RED, Layer.Background),
        'RUBY': Color.hex_to_ansi(HEXCodes.RUBY, Layer.Background),
        'RUBY_RED': Color.hex_to_ansi(HEXCodes.RUBY_RED, Layer.Background),
        'RUFOUS': Color.hex_to_ansi(HEXCodes.RUFOUS, Layer.Background),
        'RUSSET': Color.hex_to_ansi(HEXCodes.RUSSET, Layer.Background),
        'RUSSIAN_GREEN': Color.hex_to_ansi(HEXCodes.RUSSIAN_GREEN, Layer.Background),
        'RUSSIAN_VIOLET': Color.hex_to_ansi(HEXCodes.RUSSIAN_VIOLET, Layer.Background),
        'RUST': Color.hex_to_ansi(HEXCodes.RUST, Layer.Background),
        'RUSTY_RED': Color.hex_to_ansi(HEXCodes.RUSTY_RED, Layer.Background),
        'SACRAMENTO_STATE_GREEN': Color.hex_to_ansi(HEXCodes.SACRAMENTO_STATE_GREEN, Layer.Background),
        'SADDLE_BROWN': Color.hex_to_ansi(HEXCodes.SADDLE_BROWN, Layer.Background),
        'SAFETY_ORANGE': Color.hex_to_ansi(HEXCodes.SAFETY_ORANGE, Layer.Background),
        'SAFETY_ORANGE_BLAZE_ORANGE': Color.hex_to_ansi(HEXCodes.SAFETY_ORANGE_BLAZE_ORANGE, Layer.Background),
        'SAFETY_YELLOW': Color.hex_to_ansi(HEXCodes.SAFETY_YELLOW, Layer.Background),
        'SAFFRON': Color.hex_to_ansi(HEXCodes.SAFFRON, Layer.Background),
        'SAGE': Color.hex_to_ansi(HEXCodes.SAGE, Layer.Background),
        'ST_PATRICK_S_BLUE': Color.hex_to_ansi(HEXCodes.ST_PATRICK_S_BLUE, Layer.Background),
        'SALMON': Color.hex_to_ansi(HEXCodes.SALMON, Layer.Background),
        'SALMON_PINK': Color.hex_to_ansi(HEXCodes.SALMON_PINK, Layer.Background),
        'SAND': Color.hex_to_ansi(HEXCodes.SAND, Layer.Background),
        'SAND_DUNE': Color.hex_to_ansi(HEXCodes.SAND_DUNE, Layer.Background),
        'SANDY_BROWN': Color.hex_to_ansi(HEXCodes.SANDY_BROWN, Layer.Background),
        'SAP_GREEN': Color.hex_to_ansi(HEXCodes.SAP_GREEN, Layer.Background),
        'SAPPHIRE': Color.hex_to_ansi(HEXCodes.SAPPHIRE, Layer.Background),
        'SAPPHIRE_BLUE': Color.hex_to_ansi(HEXCodes.SAPPHIRE_BLUE, Layer.Background),
        'SAPPHIRE_CRAYOLA': Color.hex_to_ansi(HEXCodes.SAPPHIRE_CRAYOLA, Layer.Background),
        'SATIN_SHEEN_GOLD': Color.hex_to_ansi(HEXCodes.SATIN_SHEEN_GOLD, Layer.Background),
        'SCARLET': Color.hex_to_ansi(HEXCodes.SCARLET, Layer.Background),
        'SCHAUSS_PINK': Color.hex_to_ansi(HEXCodes.SCHAUSS_PINK, Layer.Background),
        'SCHOOL_BUS_YELLOW': Color.hex_to_ansi(HEXCodes.SCHOOL_BUS_YELLOW, Layer.Background),
        'SCREAMIN_GREEN': Color.hex_to_ansi(HEXCodes.SCREAMIN_GREEN, Layer.Background),
        'SEA_GREEN': Color.hex_to_ansi(HEXCodes.SEA_GREEN, Layer.Background),
        'SEA_GREEN_CRAYOLA': Color.hex_to_ansi(HEXCodes.SEA_GREEN_CRAYOLA, Layer.Background),
        'SEANCE': Color.hex_to_ansi(HEXCodes.SEANCE, Layer.Background),
        'SEAL_BROWN': Color.hex_to_ansi(HEXCodes.SEAL_BROWN, Layer.Background),
        'SEASHELL': Color.hex_to_ansi(HEXCodes.SEASHELL, Layer.Background),
        'SECRET': Color.hex_to_ansi(HEXCodes.SECRET, Layer.Background),
        'SELECTIVE_YELLOW': Color.hex_to_ansi(HEXCodes.SELECTIVE_YELLOW, Layer.Background),
        'SEPIA': Color.hex_to_ansi(HEXCodes.SEPIA, Layer.Background),
        'SHADOW': Color.hex_to_ansi(HEXCodes.SHADOW, Layer.Background),
        'SHADOW_BLUE': Color.hex_to_ansi(HEXCodes.SHADOW_BLUE, Layer.Background),
        'SHAMROCK_GREEN': Color.hex_to_ansi(HEXCodes.SHAMROCK_GREEN, Layer.Background),
        'SHEEN_GREEN': Color.hex_to_ansi(HEXCodes.SHEEN_GREEN, Layer.Background),
        'SHIMMERING_BLUSH': Color.hex_to_ansi(HEXCodes.SHIMMERING_BLUSH, Layer.Background),
        'SHINY_SHAMROCK': Color.hex_to_ansi(HEXCodes.SHINY_SHAMROCK, Layer.Background),
        'SHOCKING_PINK': Color.hex_to_ansi(HEXCodes.SHOCKING_PINK, Layer.Background),
        'SHOCKING_PINK_CRAYOLA': Color.hex_to_ansi(HEXCodes.SHOCKING_PINK_CRAYOLA, Layer.Background),
        'SIENNA': Color.hex_to_ansi(HEXCodes.SIENNA, Layer.Background),
        'SILVER': Color.hex_to_ansi(HEXCodes.SILVER, Layer.Background),
        'SILVER_CRAYOLA': Color.hex_to_ansi(HEXCodes.SILVER_CRAYOLA, Layer.Background),
        'SILVER_METALLIC': Color.hex_to_ansi(HEXCodes.SILVER_METALLIC, Layer.Background),
        'SILVER_CHALICE': Color.hex_to_ansi(HEXCodes.SILVER_CHALICE, Layer.Background),
        'SILVER_PINK': Color.hex_to_ansi(HEXCodes.SILVER_PINK, Layer.Background),
        'SILVER_SAND': Color.hex_to_ansi(HEXCodes.SILVER_SAND, Layer.Background),
        'SINOPIA': Color.hex_to_ansi(HEXCodes.SINOPIA, Layer.Background),
        'SIZZLING_RED': Color.hex_to_ansi(HEXCodes.SIZZLING_RED, Layer.Background),
        'SIZZLING_SUNRISE': Color.hex_to_ansi(HEXCodes.SIZZLING_SUNRISE, Layer.Background),
        'SKOBELOFF': Color.hex_to_ansi(HEXCodes.SKOBELOFF, Layer.Background),
        'SKY_BLUE': Color.hex_to_ansi(HEXCodes.SKY_BLUE, Layer.Background),
        'SKY_BLUE_CRAYOLA': Color.hex_to_ansi(HEXCodes.SKY_BLUE_CRAYOLA, Layer.Background),
        'SKY_MAGENTA': Color.hex_to_ansi(HEXCodes.SKY_MAGENTA, Layer.Background),
        'SLATE_BLUE': Color.hex_to_ansi(HEXCodes.SLATE_BLUE, Layer.Background),
        'SLATE_GRAY': Color.hex_to_ansi(HEXCodes.SLATE_GRAY, Layer.Background),
        'SLIMY_GREEN': Color.hex_to_ansi(HEXCodes.SLIMY_GREEN, Layer.Background),
        'SMITTEN': Color.hex_to_ansi(HEXCodes.SMITTEN, Layer.Background),
        'SMOKY_BLACK': Color.hex_to_ansi(HEXCodes.SMOKY_BLACK, Layer.Background),
        'SNOW': Color.hex_to_ansi(HEXCodes.SNOW, Layer.Background),
        'SOLID_PINK': Color.hex_to_ansi(HEXCodes.SOLID_PINK, Layer.Background),
        'SONIC_SILVER': Color.hex_to_ansi(HEXCodes.SONIC_SILVER, Layer.Background),
        'SPACE_CADET': Color.hex_to_ansi(HEXCodes.SPACE_CADET, Layer.Background),
        'SPANISH_BISTRE': Color.hex_to_ansi(HEXCodes.SPANISH_BISTRE, Layer.Background),
        'SPANISH_BLUE': Color.hex_to_ansi(HEXCodes.SPANISH_BLUE, Layer.Background),
        'SPANISH_CARMINE': Color.hex_to_ansi(HEXCodes.SPANISH_CARMINE, Layer.Background),
        'SPANISH_GRAY': Color.hex_to_ansi(HEXCodes.SPANISH_GRAY, Layer.Background),
        'SPANISH_GREEN': Color.hex_to_ansi(HEXCodes.SPANISH_GREEN, Layer.Background),
        'SPANISH_ORANGE': Color.hex_to_ansi(HEXCodes.SPANISH_ORANGE, Layer.Background),
        'SPANISH_PINK': Color.hex_to_ansi(HEXCodes.SPANISH_PINK, Layer.Background),
        'SPANISH_RED': Color.hex_to_ansi(HEXCodes.SPANISH_RED, Layer.Background),
        'SPANISH_SKY_BLUE': Color.hex_to_ansi(HEXCodes.SPANISH_SKY_BLUE, Layer.Background),
        'SPANISH_VIOLET': Color.hex_to_ansi(HEXCodes.SPANISH_VIOLET, Layer.Background),
        'SPANISH_VIRIDIAN': Color.hex_to_ansi(HEXCodes.SPANISH_VIRIDIAN, Layer.Background),
        'SPRING_BUD': Color.hex_to_ansi(HEXCodes.SPRING_BUD, Layer.Background),
        'SPRING_FROST': Color.hex_to_ansi(HEXCodes.SPRING_FROST, Layer.Background),
        'SPRING_GREEN': Color.hex_to_ansi(HEXCodes.SPRING_GREEN, Layer.Background),
        'SPRING_GREEN_CRAYOLA': Color.hex_to_ansi(HEXCodes.SPRING_GREEN_CRAYOLA, Layer.Background),
        'STAR_COMMAND_BLUE': Color.hex_to_ansi(HEXCodes.STAR_COMMAND_BLUE, Layer.Background),
        'STEEL_BLUE': Color.hex_to_ansi(HEXCodes.STEEL_BLUE, Layer.Background),
        'STEEL_PINK': Color.hex_to_ansi(HEXCodes.STEEL_PINK, Layer.Background),
        'STIL_DE_GRAIN_YELLOW': Color.hex_to_ansi(HEXCodes.STIL_DE_GRAIN_YELLOW, Layer.Background),
        'STIZZA': Color.hex_to_ansi(HEXCodes.STIZZA, Layer.Background),
        'STRAW': Color.hex_to_ansi(HEXCodes.STRAW, Layer.Background),
        'STRAWBERRY': Color.hex_to_ansi(HEXCodes.STRAWBERRY, Layer.Background),
        'STRAWBERRY_BLONDE': Color.hex_to_ansi(HEXCodes.STRAWBERRY_BLONDE, Layer.Background),
        'STRONG_LIME_GREEN': Color.hex_to_ansi(HEXCodes.STRONG_LIME_GREEN, Layer.Background),
        'SUGAR_PLUM': Color.hex_to_ansi(HEXCodes.SUGAR_PLUM, Layer.Background),
        'SUNGLOW': Color.hex_to_ansi(HEXCodes.SUNGLOW, Layer.Background),
        'SUNRAY': Color.hex_to_ansi(HEXCodes.SUNRAY, Layer.Background),
        'SUNSET': Color.hex_to_ansi(HEXCodes.SUNSET, Layer.Background),
        'SUPER_PINK': Color.hex_to_ansi(HEXCodes.SUPER_PINK, Layer.Background),
        'SWEET_BROWN': Color.hex_to_ansi(HEXCodes.SWEET_BROWN, Layer.Background),
        'SYRACUSE_ORANGE': Color.hex_to_ansi(HEXCodes.SYRACUSE_ORANGE, Layer.Background),
        'TAN': Color.hex_to_ansi(HEXCodes.TAN, Layer.Background),
        'TAN_CRAYOLA': Color.hex_to_ansi(HEXCodes.TAN_CRAYOLA, Layer.Background),
        'TANGERINE': Color.hex_to_ansi(HEXCodes.TANGERINE, Layer.Background),
        'TANGO_PINK': Color.hex_to_ansi(HEXCodes.TANGO_PINK, Layer.Background),
        'TART_ORANGE': Color.hex_to_ansi(HEXCodes.TART_ORANGE, Layer.Background),
        'TAUPE': Color.hex_to_ansi(HEXCodes.TAUPE, Layer.Background),
        'TAUPE_GRAY': Color.hex_to_ansi(HEXCodes.TAUPE_GRAY, Layer.Background),
        'TEA_GREEN': Color.hex_to_ansi(HEXCodes.TEA_GREEN, Layer.Background),
        'TEA_ROSE': Color.hex_to_ansi(HEXCodes.TEA_ROSE, Layer.Background),
        'TEAL': Color.hex_to_ansi(HEXCodes.TEAL, Layer.Background),
        'TEAL_BLUE': Color.hex_to_ansi(HEXCodes.TEAL_BLUE, Layer.Background),
        'TECHNOBOTANICA': Color.hex_to_ansi(HEXCodes.TECHNOBOTANICA, Layer.Background),
        'TELEMAGENTA': Color.hex_to_ansi(HEXCodes.TELEMAGENTA, Layer.Background),
        'TENNE_TAWNY': Color.hex_to_ansi(HEXCodes.TENNE_TAWNY, Layer.Background),
        'TERRA_COTTA': Color.hex_to_ansi(HEXCodes.TERRA_COTTA, Layer.Background),
        'THISTLE': Color.hex_to_ansi(HEXCodes.THISTLE, Layer.Background),
        'THULIAN_PINK': Color.hex_to_ansi(HEXCodes.THULIAN_PINK, Layer.Background),
        'TICKLE_ME_PINK': Color.hex_to_ansi(HEXCodes.TICKLE_ME_PINK, Layer.Background),
        'TIFFANY_BLUE': Color.hex_to_ansi(HEXCodes.TIFFANY_BLUE, Layer.Background),
        'TIMBERWOLF': Color.hex_to_ansi(HEXCodes.TIMBERWOLF, Layer.Background),
        'TITANIUM_YELLOW': Color.hex_to_ansi(HEXCodes.TITANIUM_YELLOW, Layer.Background),
        'TOMATO': Color.hex_to_ansi(HEXCodes.TOMATO, Layer.Background),
        'TOURMALINE': Color.hex_to_ansi(HEXCodes.TOURMALINE, Layer.Background),
        'TROPICAL_RAINFOREST': Color.hex_to_ansi(HEXCodes.TROPICAL_RAINFOREST, Layer.Background),
        'TRUE_BLUE': Color.hex_to_ansi(HEXCodes.TRUE_BLUE, Layer.Background),
        'TRYPAN_BLUE': Color.hex_to_ansi(HEXCodes.TRYPAN_BLUE, Layer.Background),
        'TUFTS_BLUE': Color.hex_to_ansi(HEXCodes.TUFTS_BLUE, Layer.Background),
        'TUMBLEWEED': Color.hex_to_ansi(HEXCodes.TUMBLEWEED, Layer.Background),
        'TURQUOISE': Color.hex_to_ansi(HEXCodes.TURQUOISE, Layer.Background),
        'TURQUOISE_BLUE': Color.hex_to_ansi(HEXCodes.TURQUOISE_BLUE, Layer.Background),
        'TURQUOISE_GREEN': Color.hex_to_ansi(HEXCodes.TURQUOISE_GREEN, Layer.Background),
        'TURTLE_GREEN': Color.hex_to_ansi(HEXCodes.TURTLE_GREEN, Layer.Background),
        'TUSCAN': Color.hex_to_ansi(HEXCodes.TUSCAN, Layer.Background),
        'TUSCAN_BROWN': Color.hex_to_ansi(HEXCodes.TUSCAN_BROWN, Layer.Background),
        'TUSCAN_RED': Color.hex_to_ansi(HEXCodes.TUSCAN_RED, Layer.Background),
        'TUSCAN_TAN': Color.hex_to_ansi(HEXCodes.TUSCAN_TAN, Layer.Background),
        'TUSCANY': Color.hex_to_ansi(HEXCodes.TUSCANY, Layer.Background),
        'TWILIGHT_LAVENDER': Color.hex_to_ansi(HEXCodes.TWILIGHT_LAVENDER, Layer.Background),
        'TYRIAN_PURPLE': Color.hex_to_ansi(HEXCodes.TYRIAN_PURPLE, Layer.Background),
        'UA_BLUE': Color.hex_to_ansi(HEXCodes.UA_BLUE, Layer.Background),
        'UA_RED': Color.hex_to_ansi(HEXCodes.UA_RED, Layer.Background),
        'ULTRAMARINE': Color.hex_to_ansi(HEXCodes.ULTRAMARINE, Layer.Background),
        'ULTRAMARINE_BLUE': Color.hex_to_ansi(HEXCodes.ULTRAMARINE_BLUE, Layer.Background),
        'ULTRA_PINK': Color.hex_to_ansi(HEXCodes.ULTRA_PINK, Layer.Background),
        'ULTRA_RED': Color.hex_to_ansi(HEXCodes.ULTRA_RED, Layer.Background),
        'UMBER': Color.hex_to_ansi(HEXCodes.UMBER, Layer.Background),
        'UNBLEACHED_SILK': Color.hex_to_ansi(HEXCodes.UNBLEACHED_SILK, Layer.Background),
        'UNITED_NATIONS_BLUE': Color.hex_to_ansi(HEXCodes.UNITED_NATIONS_BLUE, Layer.Background),
        'UNIVERSITY_OF_PENNSYLVANIA_RED': Color.hex_to_ansi(HEXCodes.UNIVERSITY_OF_PENNSYLVANIA_RED, Layer.Background),
        'UNMELLOW_YELLOW': Color.hex_to_ansi(HEXCodes.UNMELLOW_YELLOW, Layer.Background),
        'UP_FOREST_GREEN': Color.hex_to_ansi(HEXCodes.UP_FOREST_GREEN, Layer.Background),
        'UP_MAROON': Color.hex_to_ansi(HEXCodes.UP_MAROON, Layer.Background),
        'UPSDELL_RED': Color.hex_to_ansi(HEXCodes.UPSDELL_RED, Layer.Background),
        'URANIAN_BLUE': Color.hex_to_ansi(HEXCodes.URANIAN_BLUE, Layer.Background),
        'USAFA_BLUE': Color.hex_to_ansi(HEXCodes.USAFA_BLUE, Layer.Background),
        'VAN_DYKE_BROWN': Color.hex_to_ansi(HEXCodes.VAN_DYKE_BROWN, Layer.Background),
        'VANILLA': Color.hex_to_ansi(HEXCodes.VANILLA, Layer.Background),
        'VANILLA_ICE': Color.hex_to_ansi(HEXCodes.VANILLA_ICE, Layer.Background),
        'VEGAS_GOLD': Color.hex_to_ansi(HEXCodes.VEGAS_GOLD, Layer.Background),
        'VENETIAN_RED': Color.hex_to_ansi(HEXCodes.VENETIAN_RED, Layer.Background),
        'VERDIGRIS': Color.hex_to_ansi(HEXCodes.VERDIGRIS, Layer.Background),
        'VERMILION': Color.hex_to_ansi(HEXCodes.VERMILION, Layer.Background),
        'VERONICA': Color.hex_to_ansi(HEXCodes.VERONICA, Layer.Background),
        'VIOLET': Color.hex_to_ansi(HEXCodes.VIOLET, Layer.Background),
        'VIOLET_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.VIOLET_COLOR_WHEEL, Layer.Background),
        'VIOLET_CRAYOLA': Color.hex_to_ansi(HEXCodes.VIOLET_CRAYOLA, Layer.Background),
        'VIOLET_RYB': Color.hex_to_ansi(HEXCodes.VIOLET_RYB, Layer.Background),
        'VIOLET_WEB': Color.hex_to_ansi(HEXCodes.VIOLET_WEB, Layer.Background),
        'VIOLET_BLUE': Color.hex_to_ansi(HEXCodes.VIOLET_BLUE, Layer.Background),
        'VIOLET_BLUE_CRAYOLA': Color.hex_to_ansi(HEXCodes.VIOLET_BLUE_CRAYOLA, Layer.Background),
        'VIOLET_RED': Color.hex_to_ansi(HEXCodes.VIOLET_RED, Layer.Background),
        'VIOLET_REDPERBANG': Color.hex_to_ansi(HEXCodes.VIOLET_REDPERBANG, Layer.Background),
        'VIRIDIAN': Color.hex_to_ansi(HEXCodes.VIRIDIAN, Layer.Background),
        'VIRIDIAN_GREEN': Color.hex_to_ansi(HEXCodes.VIRIDIAN_GREEN, Layer.Background),
        'VIVID_BURGUNDY': Color.hex_to_ansi(HEXCodes.VIVID_BURGUNDY, Layer.Background),
        'VIVID_SKY_BLUE': Color.hex_to_ansi(HEXCodes.VIVID_SKY_BLUE, Layer.Background),
        'VIVID_TANGERINE': Color.hex_to_ansi(HEXCodes.VIVID_TANGERINE, Layer.Background),
        'VIVID_VIOLET': Color.hex_to_ansi(HEXCodes.VIVID_VIOLET, Layer.Background),
        'VOLT': Color.hex_to_ansi(HEXCodes.VOLT, Layer.Background),
        'WARM_BLACK': Color.hex_to_ansi(HEXCodes.WARM_BLACK, Layer.Background),
        'WEEZY_BLUE': Color.hex_to_ansi(HEXCodes.WEEZY_BLUE, Layer.Background),
        'WHEAT': Color.hex_to_ansi(HEXCodes.WHEAT, Layer.Background),
        'WILD_BLUE_YONDER': Color.hex_to_ansi(HEXCodes.WILD_BLUE_YONDER, Layer.Background),
        'WILD_ORCHID': Color.hex_to_ansi(HEXCodes.WILD_ORCHID, Layer.Background),
        'WILD_STRAWBERRY': Color.hex_to_ansi(HEXCodes.WILD_STRAWBERRY, Layer.Background),
        'WILD_WATERMELON': Color.hex_to_ansi(HEXCodes.WILD_WATERMELON, Layer.Background),
        'WINDSOR_TAN': Color.hex_to_ansi(HEXCodes.WINDSOR_TAN, Layer.Background),
        'WINE': Color.hex_to_ansi(HEXCodes.WINE, Layer.Background),
        'WINE_DREGS': Color.hex_to_ansi(HEXCodes.WINE_DREGS, Layer.Background),
        'WINTER_SKY': Color.hex_to_ansi(HEXCodes.WINTER_SKY, Layer.Background),
        'WINTERGREEN_DREAM': Color.hex_to_ansi(HEXCodes.WINTERGREEN_DREAM, Layer.Background),
        'WISTERIA': Color.hex_to_ansi(HEXCodes.WISTERIA, Layer.Background),
        'WOOD_BROWN': Color.hex_to_ansi(HEXCodes.WOOD_BROWN, Layer.Background),
        'XANADU': Color.hex_to_ansi(HEXCodes.XANADU, Layer.Background),
        'XANTHIC': Color.hex_to_ansi(HEXCodes.XANTHIC, Layer.Background),
        'XANTHOUS': Color.hex_to_ansi(HEXCodes.XANTHOUS, Layer.Background),
        'YALE_BLUE': Color.hex_to_ansi(HEXCodes.YALE_BLUE, Layer.Background),
        'YELLOW_CRAYOLA': Color.hex_to_ansi(HEXCodes.YELLOW_CRAYOLA, Layer.Background),
        'YELLOW_MUNSELL': Color.hex_to_ansi(HEXCodes.YELLOW_MUNSELL, Layer.Background),
        'YELLOW_NCS': Color.hex_to_ansi(HEXCodes.YELLOW_NCS, Layer.Background),
        'YELLOW_PANTONE': Color.hex_to_ansi(HEXCodes.YELLOW_PANTONE, Layer.Background),
        'YELLOW_PROCESS': Color.hex_to_ansi(HEXCodes.YELLOW_PROCESS, Layer.Background),
        'YELLOW_RYB': Color.hex_to_ansi(HEXCodes.YELLOW_RYB, Layer.Background),
        'YELLOW_GREEN': Color.hex_to_ansi(HEXCodes.YELLOW_GREEN, Layer.Background),
        'YELLOW_GREEN_CRAYOLA': Color.hex_to_ansi(HEXCodes.YELLOW_GREEN_CRAYOLA, Layer.Background),
        'YELLOW_GREEN_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.YELLOW_GREEN_COLOR_WHEEL, Layer.Background),
        'YELLOW_ORANGE': Color.hex_to_ansi(HEXCodes.YELLOW_ORANGE, Layer.Background),
        'YELLOW_ORANGE_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.YELLOW_ORANGE_COLOR_WHEEL, Layer.Background),
        'YELLOW_SUNSHINE': Color.hex_to_ansi(HEXCodes.YELLOW_SUNSHINE, Layer.Background),
        'YINMN_BLUE': Color.hex_to_ansi(HEXCodes.YINMN_BLUE, Layer.Background),
        'ZAFFRE': Color.hex_to_ansi(HEXCodes.ZAFFRE, Layer.Background),
        'ZINNWALDITE_BROWN': Color.hex_to_ansi(HEXCodes.ZINNWALDITE_BROWN, Layer.Background),
        'ZOMP': Color.hex_to_ansi(HEXCodes.ZOMP, Layer.Background)
    }

    # Constants defining standard color values
    BLACK: str = _standard_colors['BLACK']
    RED: str = _standard_colors['RED']
    GREEN: str = _standard_colors['GREEN']
    YELLOW: str = _standard_colors['YELLOW']
    BLUE: str = _standard_colors['BLUE']
    MAGENTA: str = _standard_colors['MAGENTA']
    CYAN: str = _standard_colors['CYAN']
    WHITE: str = _standard_colors['WHITE']

    # Constants defining true color values
    ABSOLUTE_ZERO: str = _true_colors['ABSOLUTE_ZERO']
    ACID_GREEN: str = _true_colors['ACID_GREEN']
    AERO: str = _true_colors['AERO']
    AFRICAN_VIOLET: str = _true_colors['AFRICAN_VIOLET']
    AIR_SUPERIORITY_BLUE: str = _true_colors['AIR_SUPERIORITY_BLUE']
    ALICE_BLUE: str = _true_colors['ALICE_BLUE']
    ALIZARIN: str = _true_colors['ALIZARIN']
    ALLOY_ORANGE: str = _true_colors['ALLOY_ORANGE']
    ALMOND: str = _true_colors['ALMOND']
    AMARANTH_DEEP_PURPLE: str = _true_colors['AMARANTH_DEEP_PURPLE']
    AMARANTH_PINK: str = _true_colors['AMARANTH_PINK']
    AMARANTH_PURPLE: str = _true_colors['AMARANTH_PURPLE']
    AMAZON: str = _true_colors['AMAZON']
    AMBER: str = _true_colors['AMBER']
    AMETHYST: str = _true_colors['AMETHYST']
    ANDROID_GREEN: str = _true_colors['ANDROID_GREEN']
    ANTIQUE_BRASS: str = _true_colors['ANTIQUE_BRASS']
    ANTIQUE_BRONZE: str = _true_colors['ANTIQUE_BRONZE']
    ANTIQUE_FUCHSIA: str = _true_colors['ANTIQUE_FUCHSIA']
    ANTIQUE_RUBY: str = _true_colors['ANTIQUE_RUBY']
    ANTIQUE_WHITE: str = _true_colors['ANTIQUE_WHITE']
    APRICOT: str = _true_colors['APRICOT']
    AQUA: str = _true_colors['AQUA']
    AQUAMARINE: str = _true_colors['AQUAMARINE']
    ARCTIC_LIME: str = _true_colors['ARCTIC_LIME']
    ARTICHOKE_GREEN: str = _true_colors['ARTICHOKE_GREEN']
    ARYLIDE_YELLOW: str = _true_colors['ARYLIDE_YELLOW']
    ASH_GRAY: str = _true_colors['ASH_GRAY']
    ATOMIC_TANGERINE: str = _true_colors['ATOMIC_TANGERINE']
    AUREOLIN: str = _true_colors['AUREOLIN']
    AZURE: str = _true_colors['AZURE']
    BABY_BLUE: str = _true_colors['BABY_BLUE']
    BABY_BLUE_EYES: str = _true_colors['BABY_BLUE_EYES']
    BABY_PINK: str = _true_colors['BABY_PINK']
    BABY_POWDER: str = _true_colors['BABY_POWDER']
    BAKER_MILLER_PINK: str = _true_colors['BAKER_MILLER_PINK']
    BANANA_MANIA: str = _true_colors['BANANA_MANIA']
    BARBIE_PINK: str = _true_colors['BARBIE_PINK']
    BARN_RED: str = _true_colors['BARN_RED']
    BATTLESHIP_GREY: str = _true_colors['BATTLESHIP_GREY']
    BEAU_BLUE: str = _true_colors['BEAU_BLUE']
    BEAVER: str = _true_colors['BEAVER']
    BEIGE: str = _true_colors['BEIGE']
    B_DAZZLED_BLUE: str = _true_colors['B_DAZZLED_BLUE']
    BIG_DIP_O_RUBY: str = _true_colors['BIG_DIP_O_RUBY']
    BISQUE: str = _true_colors['BISQUE']
    BISTRE: str = _true_colors['BISTRE']
    BISTRE_BROWN: str = _true_colors['BISTRE_BROWN']
    BITTER_LEMON: str = _true_colors['BITTER_LEMON']
    BLACK_BEAN: str = _true_colors['BLACK_BEAN']
    BLACK_CORAL: str = _true_colors['BLACK_CORAL']
    BLACK_OLIVE: str = _true_colors['BLACK_OLIVE']
    BLACK_SHADOWS: str = _true_colors['BLACK_SHADOWS']
    BLANCHED_ALMOND: str = _true_colors['BLANCHED_ALMOND']
    BLAST_OFF_BRONZE: str = _true_colors['BLAST_OFF_BRONZE']
    BLEU_DE_FRANCE: str = _true_colors['BLEU_DE_FRANCE']
    BLIZZARD_BLUE: str = _true_colors['BLIZZARD_BLUE']
    BLOOD_RED: str = _true_colors['BLOOD_RED']
    BLUE_CRAYOLA: str = _true_colors['BLUE_CRAYOLA']
    BLUE_MUNSELL: str = _true_colors['BLUE_MUNSELL']
    BLUE_NCS: str = _true_colors['BLUE_NCS']
    BLUE_PANTONE: str = _true_colors['BLUE_PANTONE']
    BLUE_PIGMENT: str = _true_colors['BLUE_PIGMENT']
    BLUE_BELL: str = _true_colors['BLUE_BELL']
    BLUE_GRAY_CRAYOLA: str = _true_colors['BLUE_GRAY_CRAYOLA']
    BLUE_JEANS: str = _true_colors['BLUE_JEANS']
    BLUE_SAPPHIRE: str = _true_colors['BLUE_SAPPHIRE']
    BLUE_VIOLET: str = _true_colors['BLUE_VIOLET']
    BLUE_YONDER: str = _true_colors['BLUE_YONDER']
    BLUETIFUL: str = _true_colors['BLUETIFUL']
    BLUSH: str = _true_colors['BLUSH']
    BOLE: str = _true_colors['BOLE']
    BONE: str = _true_colors['BONE']
    BRICK_RED: str = _true_colors['BRICK_RED']
    BRIGHT_LILAC: str = _true_colors['BRIGHT_LILAC']
    BRIGHT_YELLOW_CRAYOLA: str = _true_colors['BRIGHT_YELLOW_CRAYOLA']
    BRITISH_RACING_GREEN: str = _true_colors['BRITISH_RACING_GREEN']
    BRONZE: str = _true_colors['BRONZE']
    BROWN: str = _true_colors['BROWN']
    BROWN_SUGAR: str = _true_colors['BROWN_SUGAR']
    BUD_GREEN: str = _true_colors['BUD_GREEN']
    BUFF: str = _true_colors['BUFF']
    BURGUNDY: str = _true_colors['BURGUNDY']
    BURLYWOOD: str = _true_colors['BURLYWOOD']
    BURNISHED_BROWN: str = _true_colors['BURNISHED_BROWN']
    BURNT_ORANGE: str = _true_colors['BURNT_ORANGE']
    BURNT_SIENNA: str = _true_colors['BURNT_SIENNA']
    BURNT_UMBER: str = _true_colors['BURNT_UMBER']
    BYZANTINE: str = _true_colors['BYZANTINE']
    BYZANTIUM: str = _true_colors['BYZANTIUM']
    CADET_BLUE: str = _true_colors['CADET_BLUE']
    CADET_GREY: str = _true_colors['CADET_GREY']
    CADMIUM_GREEN: str = _true_colors['CADMIUM_GREEN']
    CADMIUM_ORANGE: str = _true_colors['CADMIUM_ORANGE']
    CAFE_AU_LAIT: str = _true_colors['CAFE_AU_LAIT']
    CAFE_NOIR: str = _true_colors['CAFE_NOIR']
    CAMBRIDGE_BLUE: str = _true_colors['CAMBRIDGE_BLUE']
    CAMEL: str = _true_colors['CAMEL']
    CAMEO_PINK: str = _true_colors['CAMEO_PINK']
    CANARY: str = _true_colors['CANARY']
    CANARY_YELLOW: str = _true_colors['CANARY_YELLOW']
    CANDY_PINK: str = _true_colors['CANDY_PINK']
    CARDINAL: str = _true_colors['CARDINAL']
    CARIBBEAN_GREEN: str = _true_colors['CARIBBEAN_GREEN']
    CARMINE: str = _true_colors['CARMINE']
    CARMINE_M_P: str = _true_colors['CARMINE_M_P']
    CARNATION_PINK: str = _true_colors['CARNATION_PINK']
    CARNELIAN: str = _true_colors['CARNELIAN']
    CAROLINA_BLUE: str = _true_colors['CAROLINA_BLUE']
    CARROT_ORANGE: str = _true_colors['CARROT_ORANGE']
    CATAWBA: str = _true_colors['CATAWBA']
    CEDAR_CHEST: str = _true_colors['CEDAR_CHEST']
    CELADON: str = _true_colors['CELADON']
    CELESTE: str = _true_colors['CELESTE']
    CERISE: str = _true_colors['CERISE']
    CERULEAN: str = _true_colors['CERULEAN']
    CERULEAN_BLUE: str = _true_colors['CERULEAN_BLUE']
    CERULEAN_FROST: str = _true_colors['CERULEAN_FROST']
    CERULEAN_CRAYOLA: str = _true_colors['CERULEAN_CRAYOLA']
    CERULEAN_RGB: str = _true_colors['CERULEAN_RGB']
    CHAMPAGNE: str = _true_colors['CHAMPAGNE']
    CHAMPAGNE_PINK: str = _true_colors['CHAMPAGNE_PINK']
    CHARCOAL: str = _true_colors['CHARCOAL']
    CHARM_PINK: str = _true_colors['CHARM_PINK']
    CHARTREUSE_WEB: str = _true_colors['CHARTREUSE_WEB']
    CHERRY_BLOSSOM_PINK: str = _true_colors['CHERRY_BLOSSOM_PINK']
    CHESTNUT: str = _true_colors['CHESTNUT']
    CHILI_RED: str = _true_colors['CHILI_RED']
    CHINA_PINK: str = _true_colors['CHINA_PINK']
    CHINESE_RED: str = _true_colors['CHINESE_RED']
    CHINESE_VIOLET: str = _true_colors['CHINESE_VIOLET']
    CHINESE_YELLOW: str = _true_colors['CHINESE_YELLOW']
    CHOCOLATE_TRADITIONAL: str = _true_colors['CHOCOLATE_TRADITIONAL']
    CHOCOLATE_WEB: str = _true_colors['CHOCOLATE_WEB']
    CINEREOUS: str = _true_colors['CINEREOUS']
    CINNABAR: str = _true_colors['CINNABAR']
    CINNAMON_SATIN: str = _true_colors['CINNAMON_SATIN']
    CITRINE: str = _true_colors['CITRINE']
    CITRON: str = _true_colors['CITRON']
    CLARET: str = _true_colors['CLARET']
    COFFEE: str = _true_colors['COFFEE']
    COLUMBIA_BLUE: str = _true_colors['COLUMBIA_BLUE']
    CONGO_PINK: str = _true_colors['CONGO_PINK']
    COOL_GREY: str = _true_colors['COOL_GREY']
    COPPER: str = _true_colors['COPPER']
    COPPER_CRAYOLA: str = _true_colors['COPPER_CRAYOLA']
    COPPER_PENNY: str = _true_colors['COPPER_PENNY']
    COPPER_RED: str = _true_colors['COPPER_RED']
    COPPER_ROSE: str = _true_colors['COPPER_ROSE']
    COQUELICOT: str = _true_colors['COQUELICOT']
    CORAL: str = _true_colors['CORAL']
    CORAL_PINK: str = _true_colors['CORAL_PINK']
    CORDOVAN: str = _true_colors['CORDOVAN']
    CORN: str = _true_colors['CORN']
    CORNFLOWER_BLUE: str = _true_colors['CORNFLOWER_BLUE']
    CORNSILK: str = _true_colors['CORNSILK']
    COSMIC_COBALT: str = _true_colors['COSMIC_COBALT']
    COSMIC_LATTE: str = _true_colors['COSMIC_LATTE']
    COYOTE_BROWN: str = _true_colors['COYOTE_BROWN']
    COTTON_CANDY: str = _true_colors['COTTON_CANDY']
    CREAM: str = _true_colors['CREAM']
    CRIMSON: str = _true_colors['CRIMSON']
    CRIMSON_UA: str = _true_colors['CRIMSON_UA']
    CULTURED_PEARL: str = _true_colors['CULTURED_PEARL']
    CYAN_PROCESS: str = _true_colors['CYAN_PROCESS']
    CYBER_GRAPE: str = _true_colors['CYBER_GRAPE']
    CYBER_YELLOW: str = _true_colors['CYBER_YELLOW']
    CYCLAMEN: str = _true_colors['CYCLAMEN']
    DANDELION: str = _true_colors['DANDELION']
    DARK_BROWN: str = _true_colors['DARK_BROWN']
    DARK_BYZANTIUM: str = _true_colors['DARK_BYZANTIUM']
    DARK_CYAN: str = _true_colors['DARK_CYAN']
    DARK_ELECTRIC_BLUE: str = _true_colors['DARK_ELECTRIC_BLUE']
    DARK_GOLDENROD: str = _true_colors['DARK_GOLDENROD']
    DARK_GREEN_X11: str = _true_colors['DARK_GREEN_X11']
    DARK_JUNGLE_GREEN: str = _true_colors['DARK_JUNGLE_GREEN']
    DARK_KHAKI: str = _true_colors['DARK_KHAKI']
    DARK_LAVA: str = _true_colors['DARK_LAVA']
    DARK_LIVER_HORSES: str = _true_colors['DARK_LIVER_HORSES']
    DARK_MAGENTA: str = _true_colors['DARK_MAGENTA']
    DARK_OLIVE_GREEN: str = _true_colors['DARK_OLIVE_GREEN']
    DARK_ORANGE: str = _true_colors['DARK_ORANGE']
    DARK_ORCHID: str = _true_colors['DARK_ORCHID']
    DARK_PURPLE: str = _true_colors['DARK_PURPLE']
    DARK_RED: str = _true_colors['DARK_RED']
    DARK_SALMON: str = _true_colors['DARK_SALMON']
    DARK_SEA_GREEN: str = _true_colors['DARK_SEA_GREEN']
    DARK_SIENNA: str = _true_colors['DARK_SIENNA']
    DARK_SKY_BLUE: str = _true_colors['DARK_SKY_BLUE']
    DARK_SLATE_BLUE: str = _true_colors['DARK_SLATE_BLUE']
    DARK_SLATE_GRAY: str = _true_colors['DARK_SLATE_GRAY']
    DARK_SPRING_GREEN: str = _true_colors['DARK_SPRING_GREEN']
    DARK_TURQUOISE: str = _true_colors['DARK_TURQUOISE']
    DARK_VIOLET: str = _true_colors['DARK_VIOLET']
    DAVY_S_GREY: str = _true_colors['DAVY_S_GREY']
    DEEP_CERISE: str = _true_colors['DEEP_CERISE']
    DEEP_CHAMPAGNE: str = _true_colors['DEEP_CHAMPAGNE']
    DEEP_CHESTNUT: str = _true_colors['DEEP_CHESTNUT']
    DEEP_JUNGLE_GREEN: str = _true_colors['DEEP_JUNGLE_GREEN']
    DEEP_PINK: str = _true_colors['DEEP_PINK']
    DEEP_SAFFRON: str = _true_colors['DEEP_SAFFRON']
    DEEP_SKY_BLUE: str = _true_colors['DEEP_SKY_BLUE']
    DEEP_SPACE_SPARKLE: str = _true_colors['DEEP_SPACE_SPARKLE']
    DEEP_TAUPE: str = _true_colors['DEEP_TAUPE']
    DENIM: str = _true_colors['DENIM']
    DENIM_BLUE: str = _true_colors['DENIM_BLUE']
    DESERT: str = _true_colors['DESERT']
    DESERT_SAND: str = _true_colors['DESERT_SAND']
    DIM_GRAY: str = _true_colors['DIM_GRAY']
    DODGER_BLUE: str = _true_colors['DODGER_BLUE']
    DRAB_DARK_BROWN: str = _true_colors['DRAB_DARK_BROWN']
    DUKE_BLUE: str = _true_colors['DUKE_BLUE']
    DUTCH_WHITE: str = _true_colors['DUTCH_WHITE']
    EBONY: str = _true_colors['EBONY']
    ECRU: str = _true_colors['ECRU']
    EERIE_BLACK: str = _true_colors['EERIE_BLACK']
    EGGPLANT: str = _true_colors['EGGPLANT']
    EGGSHELL: str = _true_colors['EGGSHELL']
    ELECTRIC_LIME: str = _true_colors['ELECTRIC_LIME']
    ELECTRIC_PURPLE: str = _true_colors['ELECTRIC_PURPLE']
    ELECTRIC_VIOLET: str = _true_colors['ELECTRIC_VIOLET']
    EMERALD: str = _true_colors['EMERALD']
    EMINENCE: str = _true_colors['EMINENCE']
    ENGLISH_LAVENDER: str = _true_colors['ENGLISH_LAVENDER']
    ENGLISH_RED: str = _true_colors['ENGLISH_RED']
    ENGLISH_VERMILLION: str = _true_colors['ENGLISH_VERMILLION']
    ENGLISH_VIOLET: str = _true_colors['ENGLISH_VIOLET']
    ERIN: str = _true_colors['ERIN']
    ETON_BLUE: str = _true_colors['ETON_BLUE']
    FALLOW: str = _true_colors['FALLOW']
    FALU_RED: str = _true_colors['FALU_RED']
    FANDANGO: str = _true_colors['FANDANGO']
    FANDANGO_PINK: str = _true_colors['FANDANGO_PINK']
    FAWN: str = _true_colors['FAWN']
    FERN_GREEN: str = _true_colors['FERN_GREEN']
    FIELD_DRAB: str = _true_colors['FIELD_DRAB']
    FIERY_ROSE: str = _true_colors['FIERY_ROSE']
    FINN: str = _true_colors['FINN']
    FIREBRICK: str = _true_colors['FIREBRICK']
    FIRE_ENGINE_RED: str = _true_colors['FIRE_ENGINE_RED']
    FLAME: str = _true_colors['FLAME']
    FLAX: str = _true_colors['FLAX']
    FLIRT: str = _true_colors['FLIRT']
    FLORAL_WHITE: str = _true_colors['FLORAL_WHITE']
    FOREST_GREEN_WEB: str = _true_colors['FOREST_GREEN_WEB']
    FRENCH_BEIGE: str = _true_colors['FRENCH_BEIGE']
    FRENCH_BISTRE: str = _true_colors['FRENCH_BISTRE']
    FRENCH_BLUE: str = _true_colors['FRENCH_BLUE']
    FRENCH_FUCHSIA: str = _true_colors['FRENCH_FUCHSIA']
    FRENCH_LILAC: str = _true_colors['FRENCH_LILAC']
    FRENCH_LIME: str = _true_colors['FRENCH_LIME']
    FRENCH_MAUVE: str = _true_colors['FRENCH_MAUVE']
    FRENCH_PINK: str = _true_colors['FRENCH_PINK']
    FRENCH_RASPBERRY: str = _true_colors['FRENCH_RASPBERRY']
    FRENCH_SKY_BLUE: str = _true_colors['FRENCH_SKY_BLUE']
    FRENCH_VIOLET: str = _true_colors['FRENCH_VIOLET']
    FROSTBITE: str = _true_colors['FROSTBITE']
    FUCHSIA: str = _true_colors['FUCHSIA']
    FUCHSIA_CRAYOLA: str = _true_colors['FUCHSIA_CRAYOLA']
    FULVOUS: str = _true_colors['FULVOUS']
    FUZZY_WUZZY: str = _true_colors['FUZZY_WUZZY']
    GAINSBORO: str = _true_colors['GAINSBORO']
    GAMBOGE: str = _true_colors['GAMBOGE']
    GENERIC_VIRIDIAN: str = _true_colors['GENERIC_VIRIDIAN']
    GHOST_WHITE: str = _true_colors['GHOST_WHITE']
    GLAUCOUS: str = _true_colors['GLAUCOUS']
    GLOSSY_GRAPE: str = _true_colors['GLOSSY_GRAPE']
    GO_GREEN: str = _true_colors['GO_GREEN']
    GOLD_METALLIC: str = _true_colors['GOLD_METALLIC']
    GOLD_WEB_GOLDEN: str = _true_colors['GOLD_WEB_GOLDEN']
    GOLD_CRAYOLA: str = _true_colors['GOLD_CRAYOLA']
    GOLD_FUSION: str = _true_colors['GOLD_FUSION']
    GOLDEN_BROWN: str = _true_colors['GOLDEN_BROWN']
    GOLDEN_POPPY: str = _true_colors['GOLDEN_POPPY']
    GOLDEN_YELLOW: str = _true_colors['GOLDEN_YELLOW']
    GOLDENROD: str = _true_colors['GOLDENROD']
    GOTHAM_GREEN: str = _true_colors['GOTHAM_GREEN']
    GRANITE_GRAY: str = _true_colors['GRANITE_GRAY']
    GRANNY_SMITH_APPLE: str = _true_colors['GRANNY_SMITH_APPLE']
    GRAY_WEB: str = _true_colors['GRAY_WEB']
    GRAY_X11_GRAY: str = _true_colors['GRAY_X11_GRAY']
    GREEN_CRAYOLA: str = _true_colors['GREEN_CRAYOLA']
    GREEN_WEB: str = _true_colors['GREEN_WEB']
    GREEN_MUNSELL: str = _true_colors['GREEN_MUNSELL']
    GREEN_NCS: str = _true_colors['GREEN_NCS']
    GREEN_PANTONE: str = _true_colors['GREEN_PANTONE']
    GREEN_PIGMENT: str = _true_colors['GREEN_PIGMENT']
    GREEN_BLUE: str = _true_colors['GREEN_BLUE']
    GREEN_LIZARD: str = _true_colors['GREEN_LIZARD']
    GREEN_SHEEN: str = _true_colors['GREEN_SHEEN']
    GUNMETAL: str = _true_colors['GUNMETAL']
    HANSA_YELLOW: str = _true_colors['HANSA_YELLOW']
    HARLEQUIN: str = _true_colors['HARLEQUIN']
    HARVEST_GOLD: str = _true_colors['HARVEST_GOLD']
    HEAT_WAVE: str = _true_colors['HEAT_WAVE']
    HELIOTROPE: str = _true_colors['HELIOTROPE']
    HELIOTROPE_GRAY: str = _true_colors['HELIOTROPE_GRAY']
    HOLLYWOOD_CERISE: str = _true_colors['HOLLYWOOD_CERISE']
    HONOLULU_BLUE: str = _true_colors['HONOLULU_BLUE']
    HOOKER_S_GREEN: str = _true_colors['HOOKER_S_GREEN']
    HOT_MAGENTA: str = _true_colors['HOT_MAGENTA']
    HOT_PINK: str = _true_colors['HOT_PINK']
    HUNTER_GREEN: str = _true_colors['HUNTER_GREEN']
    ICEBERG: str = _true_colors['ICEBERG']
    ILLUMINATING_EMERALD: str = _true_colors['ILLUMINATING_EMERALD']
    IMPERIAL_RED: str = _true_colors['IMPERIAL_RED']
    INCHWORM: str = _true_colors['INCHWORM']
    INDEPENDENCE: str = _true_colors['INDEPENDENCE']
    INDIA_GREEN: str = _true_colors['INDIA_GREEN']
    INDIAN_RED: str = _true_colors['INDIAN_RED']
    INDIAN_YELLOW: str = _true_colors['INDIAN_YELLOW']
    INDIGO: str = _true_colors['INDIGO']
    INDIGO_DYE: str = _true_colors['INDIGO_DYE']
    INTERNATIONAL_KLEIN_BLUE: str = _true_colors['INTERNATIONAL_KLEIN_BLUE']
    INTERNATIONAL_ORANGE_ENGINEERING: str = _true_colors['INTERNATIONAL_ORANGE_ENGINEERING']
    INTERNATIONAL_ORANGE_GOLDEN_GATE_BRIDGE: str = _true_colors['INTERNATIONAL_ORANGE_GOLDEN_GATE_BRIDGE']
    IRRESISTIBLE: str = _true_colors['IRRESISTIBLE']
    ISABELLINE: str = _true_colors['ISABELLINE']
    ITALIAN_SKY_BLUE: str = _true_colors['ITALIAN_SKY_BLUE']
    IVORY: str = _true_colors['IVORY']
    JAPANESE_CARMINE: str = _true_colors['JAPANESE_CARMINE']
    JAPANESE_VIOLET: str = _true_colors['JAPANESE_VIOLET']
    JASMINE: str = _true_colors['JASMINE']
    JAZZBERRY_JAM: str = _true_colors['JAZZBERRY_JAM']
    JET: str = _true_colors['JET']
    JONQUIL: str = _true_colors['JONQUIL']
    JUNE_BUD: str = _true_colors['JUNE_BUD']
    JUNGLE_GREEN: str = _true_colors['JUNGLE_GREEN']
    KELLY_GREEN: str = _true_colors['KELLY_GREEN']
    KEPPEL: str = _true_colors['KEPPEL']
    KEY_LIME: str = _true_colors['KEY_LIME']
    KHAKI_WEB: str = _true_colors['KHAKI_WEB']
    KHAKI_X11_LIGHT_KHAKI: str = _true_colors['KHAKI_X11_LIGHT_KHAKI']
    KOBE: str = _true_colors['KOBE']
    KOBI: str = _true_colors['KOBI']
    KOBICHA: str = _true_colors['KOBICHA']
    KSU_PURPLE: str = _true_colors['KSU_PURPLE']
    LANGUID_LAVENDER: str = _true_colors['LANGUID_LAVENDER']
    LAPIS_LAZULI: str = _true_colors['LAPIS_LAZULI']
    LASER_LEMON: str = _true_colors['LASER_LEMON']
    LAUREL_GREEN: str = _true_colors['LAUREL_GREEN']
    LAVA: str = _true_colors['LAVA']
    LAVENDER_FLORAL: str = _true_colors['LAVENDER_FLORAL']
    LAVENDER_WEB: str = _true_colors['LAVENDER_WEB']
    LAVENDER_BLUE: str = _true_colors['LAVENDER_BLUE']
    LAVENDER_BLUSH: str = _true_colors['LAVENDER_BLUSH']
    LAVENDER_GRAY: str = _true_colors['LAVENDER_GRAY']
    LAWN_GREEN: str = _true_colors['LAWN_GREEN']
    LEMON: str = _true_colors['LEMON']
    LEMON_CHIFFON: str = _true_colors['LEMON_CHIFFON']
    LEMON_CURRY: str = _true_colors['LEMON_CURRY']
    LEMON_GLACIER: str = _true_colors['LEMON_GLACIER']
    LEMON_MERINGUE: str = _true_colors['LEMON_MERINGUE']
    LEMON_YELLOW: str = _true_colors['LEMON_YELLOW']
    LEMON_YELLOW_CRAYOLA: str = _true_colors['LEMON_YELLOW_CRAYOLA']
    LIBERTY: str = _true_colors['LIBERTY']
    LIGHT_BLUE: str = _true_colors['LIGHT_BLUE']
    LIGHT_CORAL: str = _true_colors['LIGHT_CORAL']
    LIGHT_CORNFLOWER_BLUE: str = _true_colors['LIGHT_CORNFLOWER_BLUE']
    LIGHT_CYAN: str = _true_colors['LIGHT_CYAN']
    LIGHT_FRENCH_BEIGE: str = _true_colors['LIGHT_FRENCH_BEIGE']
    LIGHT_GOLDENROD_YELLOW: str = _true_colors['LIGHT_GOLDENROD_YELLOW']
    LIGHT_GRAY: str = _true_colors['LIGHT_GRAY']
    LIGHT_GREEN: str = _true_colors['LIGHT_GREEN']
    LIGHT_ORANGE: str = _true_colors['LIGHT_ORANGE']
    LIGHT_PERIWINKLE: str = _true_colors['LIGHT_PERIWINKLE']
    LIGHT_PINK: str = _true_colors['LIGHT_PINK']
    LIGHT_SALMON: str = _true_colors['LIGHT_SALMON']
    LIGHT_SEA_GREEN: str = _true_colors['LIGHT_SEA_GREEN']
    LIGHT_SKY_BLUE: str = _true_colors['LIGHT_SKY_BLUE']
    LIGHT_SLATE_GRAY: str = _true_colors['LIGHT_SLATE_GRAY']
    LIGHT_STEEL_BLUE: str = _true_colors['LIGHT_STEEL_BLUE']
    LIGHT_YELLOW: str = _true_colors['LIGHT_YELLOW']
    LILAC: str = _true_colors['LILAC']
    LILAC_LUSTER: str = _true_colors['LILAC_LUSTER']
    LIME_COLOR_WHEEL: str = _true_colors['LIME_COLOR_WHEEL']
    LIME_WEB_X11_GREEN: str = _true_colors['LIME_WEB_X11_GREEN']
    LIME_GREEN: str = _true_colors['LIME_GREEN']
    LINCOLN_GREEN: str = _true_colors['LINCOLN_GREEN']
    LINEN: str = _true_colors['LINEN']
    LION: str = _true_colors['LION']
    LISERAN_PURPLE: str = _true_colors['LISERAN_PURPLE']
    LITTLE_BOY_BLUE: str = _true_colors['LITTLE_BOY_BLUE']
    LIVER: str = _true_colors['LIVER']
    LIVER_DOGS: str = _true_colors['LIVER_DOGS']
    LIVER_ORGAN: str = _true_colors['LIVER_ORGAN']
    LIVER_CHESTNUT: str = _true_colors['LIVER_CHESTNUT']
    LIVID: str = _true_colors['LIVID']
    MACARONI_AND_CHEESE: str = _true_colors['MACARONI_AND_CHEESE']
    MADDER_LAKE: str = _true_colors['MADDER_LAKE']
    MAGENTA_CRAYOLA: str = _true_colors['MAGENTA_CRAYOLA']
    MAGENTA_DYE: str = _true_colors['MAGENTA_DYE']
    MAGENTA_PANTONE: str = _true_colors['MAGENTA_PANTONE']
    MAGENTA_PROCESS: str = _true_colors['MAGENTA_PROCESS']
    MAGENTA_HAZE: str = _true_colors['MAGENTA_HAZE']
    MAGIC_MINT: str = _true_colors['MAGIC_MINT']
    MAGNOLIA: str = _true_colors['MAGNOLIA']
    MAHOGANY: str = _true_colors['MAHOGANY']
    MAIZE: str = _true_colors['MAIZE']
    MAIZE_CRAYOLA: str = _true_colors['MAIZE_CRAYOLA']
    MAJORELLE_BLUE: str = _true_colors['MAJORELLE_BLUE']
    MALACHITE: str = _true_colors['MALACHITE']
    MANATEE: str = _true_colors['MANATEE']
    MANDARIN: str = _true_colors['MANDARIN']
    MANGO: str = _true_colors['MANGO']
    MANGO_TANGO: str = _true_colors['MANGO_TANGO']
    MANTIS: str = _true_colors['MANTIS']
    MARDI_GRAS: str = _true_colors['MARDI_GRAS']
    MARIGOLD: str = _true_colors['MARIGOLD']
    MAROON_CRAYOLA: str = _true_colors['MAROON_CRAYOLA']
    MAROON_WEB: str = _true_colors['MAROON_WEB']
    MAROON_X11: str = _true_colors['MAROON_X11']
    MAUVE: str = _true_colors['MAUVE']
    MAUVE_TAUPE: str = _true_colors['MAUVE_TAUPE']
    MAUVELOUS: str = _true_colors['MAUVELOUS']
    MAXIMUM_BLUE: str = _true_colors['MAXIMUM_BLUE']
    MAXIMUM_BLUE_GREEN: str = _true_colors['MAXIMUM_BLUE_GREEN']
    MAXIMUM_BLUE_PURPLE: str = _true_colors['MAXIMUM_BLUE_PURPLE']
    MAXIMUM_GREEN: str = _true_colors['MAXIMUM_GREEN']
    MAXIMUM_GREEN_YELLOW: str = _true_colors['MAXIMUM_GREEN_YELLOW']
    MAXIMUM_PURPLE: str = _true_colors['MAXIMUM_PURPLE']
    MAXIMUM_RED: str = _true_colors['MAXIMUM_RED']
    MAXIMUM_RED_PURPLE: str = _true_colors['MAXIMUM_RED_PURPLE']
    MAXIMUM_YELLOW: str = _true_colors['MAXIMUM_YELLOW']
    MAXIMUM_YELLOW_RED: str = _true_colors['MAXIMUM_YELLOW_RED']
    MAY_GREEN: str = _true_colors['MAY_GREEN']
    MAYA_BLUE: str = _true_colors['MAYA_BLUE']
    MEDIUM_AQUAMARINE: str = _true_colors['MEDIUM_AQUAMARINE']
    MEDIUM_BLUE: str = _true_colors['MEDIUM_BLUE']
    MEDIUM_CANDY_APPLE_RED: str = _true_colors['MEDIUM_CANDY_APPLE_RED']
    MEDIUM_CARMINE: str = _true_colors['MEDIUM_CARMINE']
    MEDIUM_CHAMPAGNE: str = _true_colors['MEDIUM_CHAMPAGNE']
    MEDIUM_ORCHID: str = _true_colors['MEDIUM_ORCHID']
    MEDIUM_PURPLE: str = _true_colors['MEDIUM_PURPLE']
    MEDIUM_SEA_GREEN: str = _true_colors['MEDIUM_SEA_GREEN']
    MEDIUM_SLATE_BLUE: str = _true_colors['MEDIUM_SLATE_BLUE']
    MEDIUM_SPRING_GREEN: str = _true_colors['MEDIUM_SPRING_GREEN']
    MEDIUM_TURQUOISE: str = _true_colors['MEDIUM_TURQUOISE']
    MEDIUM_VIOLET_RED: str = _true_colors['MEDIUM_VIOLET_RED']
    MELLOW_APRICOT: str = _true_colors['MELLOW_APRICOT']
    MELLOW_YELLOW: str = _true_colors['MELLOW_YELLOW']
    MELON: str = _true_colors['MELON']
    METALLIC_GOLD: str = _true_colors['METALLIC_GOLD']
    METALLIC_SEAWEED: str = _true_colors['METALLIC_SEAWEED']
    METALLIC_SUNBURST: str = _true_colors['METALLIC_SUNBURST']
    MEXICAN_PINK: str = _true_colors['MEXICAN_PINK']
    MIDDLE_BLUE: str = _true_colors['MIDDLE_BLUE']
    MIDDLE_BLUE_GREEN: str = _true_colors['MIDDLE_BLUE_GREEN']
    MIDDLE_BLUE_PURPLE: str = _true_colors['MIDDLE_BLUE_PURPLE']
    MIDDLE_GREY: str = _true_colors['MIDDLE_GREY']
    MIDDLE_GREEN: str = _true_colors['MIDDLE_GREEN']
    MIDDLE_GREEN_YELLOW: str = _true_colors['MIDDLE_GREEN_YELLOW']
    MIDDLE_PURPLE: str = _true_colors['MIDDLE_PURPLE']
    MIDDLE_RED: str = _true_colors['MIDDLE_RED']
    MIDDLE_RED_PURPLE: str = _true_colors['MIDDLE_RED_PURPLE']
    MIDDLE_YELLOW: str = _true_colors['MIDDLE_YELLOW']
    MIDDLE_YELLOW_RED: str = _true_colors['MIDDLE_YELLOW_RED']
    MIDNIGHT: str = _true_colors['MIDNIGHT']
    MIDNIGHT_BLUE: str = _true_colors['MIDNIGHT_BLUE']
    MIDNIGHT_GREEN_EAGLE_GREEN: str = _true_colors['MIDNIGHT_GREEN_EAGLE_GREEN']
    MIKADO_YELLOW: str = _true_colors['MIKADO_YELLOW']
    MIMI_PINK: str = _true_colors['MIMI_PINK']
    MINDARO: str = _true_colors['MINDARO']
    MING: str = _true_colors['MING']
    MINION_YELLOW: str = _true_colors['MINION_YELLOW']
    MINT: str = _true_colors['MINT']
    MINT_CREAM: str = _true_colors['MINT_CREAM']
    MINT_GREEN: str = _true_colors['MINT_GREEN']
    MISTY_MOSS: str = _true_colors['MISTY_MOSS']
    MISTY_ROSE: str = _true_colors['MISTY_ROSE']
    MODE_BEIGE: str = _true_colors['MODE_BEIGE']
    MONA_LISA: str = _true_colors['MONA_LISA']
    MORNING_BLUE: str = _true_colors['MORNING_BLUE']
    MOSS_GREEN: str = _true_colors['MOSS_GREEN']
    MOUNTAIN_MEADOW: str = _true_colors['MOUNTAIN_MEADOW']
    MOUNTBATTEN_PINK: str = _true_colors['MOUNTBATTEN_PINK']
    MSU_GREEN: str = _true_colors['MSU_GREEN']
    MULBERRY: str = _true_colors['MULBERRY']
    MULBERRY_CRAYOLA: str = _true_colors['MULBERRY_CRAYOLA']
    MUSTARD: str = _true_colors['MUSTARD']
    MYRTLE_GREEN: str = _true_colors['MYRTLE_GREEN']
    MYSTIC: str = _true_colors['MYSTIC']
    MYSTIC_MAROON: str = _true_colors['MYSTIC_MAROON']
    NADESHIKO_PINK: str = _true_colors['NADESHIKO_PINK']
    NAPLES_YELLOW: str = _true_colors['NAPLES_YELLOW']
    NAVAJO_WHITE: str = _true_colors['NAVAJO_WHITE']
    NAVY_BLUE: str = _true_colors['NAVY_BLUE']
    NAVY_BLUE_CRAYOLA: str = _true_colors['NAVY_BLUE_CRAYOLA']
    NEON_BLUE: str = _true_colors['NEON_BLUE']
    NEON_GREEN: str = _true_colors['NEON_GREEN']
    NEON_FUCHSIA: str = _true_colors['NEON_FUCHSIA']
    NEW_CAR: str = _true_colors['NEW_CAR']
    NEW_YORK_PINK: str = _true_colors['NEW_YORK_PINK']
    NICKEL: str = _true_colors['NICKEL']
    NON_PHOTO_BLUE: str = _true_colors['NON_PHOTO_BLUE']
    NYANZA: str = _true_colors['NYANZA']
    OCHRE: str = _true_colors['OCHRE']
    OLD_BURGUNDY: str = _true_colors['OLD_BURGUNDY']
    OLD_GOLD: str = _true_colors['OLD_GOLD']
    OLD_LACE: str = _true_colors['OLD_LACE']
    OLD_LAVENDER: str = _true_colors['OLD_LAVENDER']
    OLD_MAUVE: str = _true_colors['OLD_MAUVE']
    OLD_ROSE: str = _true_colors['OLD_ROSE']
    OLD_SILVER: str = _true_colors['OLD_SILVER']
    OLIVE: str = _true_colors['OLIVE']
    OLIVE_DRAB_3: str = _true_colors['OLIVE_DRAB_3']
    OLIVE_DRAB_7: str = _true_colors['OLIVE_DRAB_7']
    OLIVE_GREEN: str = _true_colors['OLIVE_GREEN']
    OLIVINE: str = _true_colors['OLIVINE']
    ONYX: str = _true_colors['ONYX']
    OPAL: str = _true_colors['OPAL']
    OPERA_MAUVE: str = _true_colors['OPERA_MAUVE']
    ORANGE: str = _true_colors['ORANGE']
    ORANGE_CRAYOLA: str = _true_colors['ORANGE_CRAYOLA']
    ORANGE_PANTONE: str = _true_colors['ORANGE_PANTONE']
    ORANGE_WEB: str = _true_colors['ORANGE_WEB']
    ORANGE_PEEL: str = _true_colors['ORANGE_PEEL']
    ORANGE_RED: str = _true_colors['ORANGE_RED']
    ORANGE_RED_CRAYOLA: str = _true_colors['ORANGE_RED_CRAYOLA']
    ORANGE_SODA: str = _true_colors['ORANGE_SODA']
    ORANGE_YELLOW: str = _true_colors['ORANGE_YELLOW']
    ORANGE_YELLOW_CRAYOLA: str = _true_colors['ORANGE_YELLOW_CRAYOLA']
    ORCHID: str = _true_colors['ORCHID']
    ORCHID_PINK: str = _true_colors['ORCHID_PINK']
    ORCHID_CRAYOLA: str = _true_colors['ORCHID_CRAYOLA']
    OUTER_SPACE_CRAYOLA: str = _true_colors['OUTER_SPACE_CRAYOLA']
    OUTRAGEOUS_ORANGE: str = _true_colors['OUTRAGEOUS_ORANGE']
    OXBLOOD: str = _true_colors['OXBLOOD']
    OXFORD_BLUE: str = _true_colors['OXFORD_BLUE']
    OU_CRIMSON_RED: str = _true_colors['OU_CRIMSON_RED']
    PACIFIC_BLUE: str = _true_colors['PACIFIC_BLUE']
    PAKISTAN_GREEN: str = _true_colors['PAKISTAN_GREEN']
    PALATINATE_PURPLE: str = _true_colors['PALATINATE_PURPLE']
    PALE_AQUA: str = _true_colors['PALE_AQUA']
    PALE_CERULEAN: str = _true_colors['PALE_CERULEAN']
    PALE_DOGWOOD: str = _true_colors['PALE_DOGWOOD']
    PALE_PINK: str = _true_colors['PALE_PINK']
    PALE_PURPLE_PANTONE: str = _true_colors['PALE_PURPLE_PANTONE']
    PALE_SPRING_BUD: str = _true_colors['PALE_SPRING_BUD']
    PANSY_PURPLE: str = _true_colors['PANSY_PURPLE']
    PAOLO_VERONESE_GREEN: str = _true_colors['PAOLO_VERONESE_GREEN']
    PAPAYA_WHIP: str = _true_colors['PAPAYA_WHIP']
    PARADISE_PINK: str = _true_colors['PARADISE_PINK']
    PARCHMENT: str = _true_colors['PARCHMENT']
    PARIS_GREEN: str = _true_colors['PARIS_GREEN']
    PASTEL_PINK: str = _true_colors['PASTEL_PINK']
    PATRIARCH: str = _true_colors['PATRIARCH']
    PAUA: str = _true_colors['PAUA']
    PAYNE_S_GREY: str = _true_colors['PAYNE_S_GREY']
    PEACH: str = _true_colors['PEACH']
    PEACH_CRAYOLA: str = _true_colors['PEACH_CRAYOLA']
    PEACH_PUFF: str = _true_colors['PEACH_PUFF']
    PEAR: str = _true_colors['PEAR']
    PEARLY_PURPLE: str = _true_colors['PEARLY_PURPLE']
    PERIWINKLE: str = _true_colors['PERIWINKLE']
    PERIWINKLE_CRAYOLA: str = _true_colors['PERIWINKLE_CRAYOLA']
    PERMANENT_GERANIUM_LAKE: str = _true_colors['PERMANENT_GERANIUM_LAKE']
    PERSIAN_BLUE: str = _true_colors['PERSIAN_BLUE']
    PERSIAN_GREEN: str = _true_colors['PERSIAN_GREEN']
    PERSIAN_INDIGO: str = _true_colors['PERSIAN_INDIGO']
    PERSIAN_ORANGE: str = _true_colors['PERSIAN_ORANGE']
    PERSIAN_PINK: str = _true_colors['PERSIAN_PINK']
    PERSIAN_PLUM: str = _true_colors['PERSIAN_PLUM']
    PERSIAN_RED: str = _true_colors['PERSIAN_RED']
    PERSIAN_ROSE: str = _true_colors['PERSIAN_ROSE']
    PERSIMMON: str = _true_colors['PERSIMMON']
    PEWTER_BLUE: str = _true_colors['PEWTER_BLUE']
    PHLOX: str = _true_colors['PHLOX']
    PHTHALO_BLUE: str = _true_colors['PHTHALO_BLUE']
    PHTHALO_GREEN: str = _true_colors['PHTHALO_GREEN']
    PICOTEE_BLUE: str = _true_colors['PICOTEE_BLUE']
    PICTORIAL_CARMINE: str = _true_colors['PICTORIAL_CARMINE']
    PIGGY_PINK: str = _true_colors['PIGGY_PINK']
    PINE_GREEN: str = _true_colors['PINE_GREEN']
    PINK: str = _true_colors['PINK']
    PINK_PANTONE: str = _true_colors['PINK_PANTONE']
    PINK_LACE: str = _true_colors['PINK_LACE']
    PINK_LAVENDER: str = _true_colors['PINK_LAVENDER']
    PINK_SHERBET: str = _true_colors['PINK_SHERBET']
    PISTACHIO: str = _true_colors['PISTACHIO']
    PLATINUM: str = _true_colors['PLATINUM']
    PLUM: str = _true_colors['PLUM']
    PLUM_WEB: str = _true_colors['PLUM_WEB']
    PLUMP_PURPLE: str = _true_colors['PLUMP_PURPLE']
    POLISHED_PINE: str = _true_colors['POLISHED_PINE']
    POMP_AND_POWER: str = _true_colors['POMP_AND_POWER']
    POPSTAR: str = _true_colors['POPSTAR']
    PORTLAND_ORANGE: str = _true_colors['PORTLAND_ORANGE']
    POWDER_BLUE: str = _true_colors['POWDER_BLUE']
    PRAIRIE_GOLD: str = _true_colors['PRAIRIE_GOLD']
    PRINCETON_ORANGE: str = _true_colors['PRINCETON_ORANGE']
    PRUNE: str = _true_colors['PRUNE']
    PRUSSIAN_BLUE: str = _true_colors['PRUSSIAN_BLUE']
    PSYCHEDELIC_PURPLE: str = _true_colors['PSYCHEDELIC_PURPLE']
    PUCE: str = _true_colors['PUCE']
    PULLMAN_BROWN_UPS_BROWN: str = _true_colors['PULLMAN_BROWN_UPS_BROWN']
    PUMPKIN: str = _true_colors['PUMPKIN']
    PURPLE: str = _true_colors['PURPLE']
    PURPLE_WEB: str = _true_colors['PURPLE_WEB']
    PURPLE_MUNSELL: str = _true_colors['PURPLE_MUNSELL']
    PURPLE_X11: str = _true_colors['PURPLE_X11']
    PURPLE_MOUNTAIN_MAJESTY: str = _true_colors['PURPLE_MOUNTAIN_MAJESTY']
    PURPLE_NAVY: str = _true_colors['PURPLE_NAVY']
    PURPLE_PIZZAZZ: str = _true_colors['PURPLE_PIZZAZZ']
    PURPLE_PLUM: str = _true_colors['PURPLE_PLUM']
    PURPUREUS: str = _true_colors['PURPUREUS']
    QUEEN_BLUE: str = _true_colors['QUEEN_BLUE']
    QUEEN_PINK: str = _true_colors['QUEEN_PINK']
    QUICK_SILVER: str = _true_colors['QUICK_SILVER']
    QUINACRIDONE_MAGENTA: str = _true_colors['QUINACRIDONE_MAGENTA']
    RADICAL_RED: str = _true_colors['RADICAL_RED']
    RAISIN_BLACK: str = _true_colors['RAISIN_BLACK']
    RAJAH: str = _true_colors['RAJAH']
    RASPBERRY: str = _true_colors['RASPBERRY']
    RASPBERRY_GLACE: str = _true_colors['RASPBERRY_GLACE']
    RASPBERRY_ROSE: str = _true_colors['RASPBERRY_ROSE']
    RAW_SIENNA: str = _true_colors['RAW_SIENNA']
    RAW_UMBER: str = _true_colors['RAW_UMBER']
    RAZZLE_DAZZLE_ROSE: str = _true_colors['RAZZLE_DAZZLE_ROSE']
    RAZZMATAZZ: str = _true_colors['RAZZMATAZZ']
    RAZZMIC_BERRY: str = _true_colors['RAZZMIC_BERRY']
    REBECCA_PURPLE: str = _true_colors['REBECCA_PURPLE']
    RED_CRAYOLA: str = _true_colors['RED_CRAYOLA']
    RED_MUNSELL: str = _true_colors['RED_MUNSELL']
    RED_NCS: str = _true_colors['RED_NCS']
    RED_PANTONE: str = _true_colors['RED_PANTONE']
    RED_PIGMENT: str = _true_colors['RED_PIGMENT']
    RED_RYB: str = _true_colors['RED_RYB']
    RED_ORANGE: str = _true_colors['RED_ORANGE']
    RED_ORANGE_CRAYOLA: str = _true_colors['RED_ORANGE_CRAYOLA']
    RED_ORANGE_COLOR_WHEEL: str = _true_colors['RED_ORANGE_COLOR_WHEEL']
    RED_PURPLE: str = _true_colors['RED_PURPLE']
    RED_SALSA: str = _true_colors['RED_SALSA']
    RED_VIOLET: str = _true_colors['RED_VIOLET']
    RED_VIOLET_CRAYOLA: str = _true_colors['RED_VIOLET_CRAYOLA']
    RED_VIOLET_COLOR_WHEEL: str = _true_colors['RED_VIOLET_COLOR_WHEEL']
    REDWOOD: str = _true_colors['REDWOOD']
    RESOLUTION_BLUE: str = _true_colors['RESOLUTION_BLUE']
    RHYTHM: str = _true_colors['RHYTHM']
    RICH_BLACK: str = _true_colors['RICH_BLACK']
    RICH_BLACK_FOGRA29: str = _true_colors['RICH_BLACK_FOGRA29']
    RICH_BLACK_FOGRA39: str = _true_colors['RICH_BLACK_FOGRA39']
    RIFLE_GREEN: str = _true_colors['RIFLE_GREEN']
    ROBIN_EGG_BLUE: str = _true_colors['ROBIN_EGG_BLUE']
    ROCKET_METALLIC: str = _true_colors['ROCKET_METALLIC']
    ROJO_SPANISH_RED: str = _true_colors['ROJO_SPANISH_RED']
    ROMAN_SILVER: str = _true_colors['ROMAN_SILVER']
    ROSE: str = _true_colors['ROSE']
    ROSE_BONBON: str = _true_colors['ROSE_BONBON']
    ROSE_DUST: str = _true_colors['ROSE_DUST']
    ROSE_EBONY: str = _true_colors['ROSE_EBONY']
    ROSE_MADDER: str = _true_colors['ROSE_MADDER']
    ROSE_PINK: str = _true_colors['ROSE_PINK']
    ROSE_POMPADOUR: str = _true_colors['ROSE_POMPADOUR']
    ROSE_RED: str = _true_colors['ROSE_RED']
    ROSE_TAUPE: str = _true_colors['ROSE_TAUPE']
    ROSE_VALE: str = _true_colors['ROSE_VALE']
    ROSEWOOD: str = _true_colors['ROSEWOOD']
    ROSSO_CORSA: str = _true_colors['ROSSO_CORSA']
    ROSY_BROWN: str = _true_colors['ROSY_BROWN']
    ROYAL_BLUE_DARK: str = _true_colors['ROYAL_BLUE_DARK']
    ROYAL_BLUE_LIGHT: str = _true_colors['ROYAL_BLUE_LIGHT']
    ROYAL_PURPLE: str = _true_colors['ROYAL_PURPLE']
    ROYAL_YELLOW: str = _true_colors['ROYAL_YELLOW']
    RUBER: str = _true_colors['RUBER']
    RUBINE_RED: str = _true_colors['RUBINE_RED']
    RUBY: str = _true_colors['RUBY']
    RUBY_RED: str = _true_colors['RUBY_RED']
    RUFOUS: str = _true_colors['RUFOUS']
    RUSSET: str = _true_colors['RUSSET']
    RUSSIAN_GREEN: str = _true_colors['RUSSIAN_GREEN']
    RUSSIAN_VIOLET: str = _true_colors['RUSSIAN_VIOLET']
    RUST: str = _true_colors['RUST']
    RUSTY_RED: str = _true_colors['RUSTY_RED']
    SACRAMENTO_STATE_GREEN: str = _true_colors['SACRAMENTO_STATE_GREEN']
    SADDLE_BROWN: str = _true_colors['SADDLE_BROWN']
    SAFETY_ORANGE: str = _true_colors['SAFETY_ORANGE']
    SAFETY_ORANGE_BLAZE_ORANGE: str = _true_colors['SAFETY_ORANGE_BLAZE_ORANGE']
    SAFETY_YELLOW: str = _true_colors['SAFETY_YELLOW']
    SAFFRON: str = _true_colors['SAFFRON']
    SAGE: str = _true_colors['SAGE']
    ST_PATRICK_S_BLUE: str = _true_colors['ST_PATRICK_S_BLUE']
    SALMON: str = _true_colors['SALMON']
    SALMON_PINK: str = _true_colors['SALMON_PINK']
    SAND: str = _true_colors['SAND']
    SAND_DUNE: str = _true_colors['SAND_DUNE']
    SANDY_BROWN: str = _true_colors['SANDY_BROWN']
    SAP_GREEN: str = _true_colors['SAP_GREEN']
    SAPPHIRE: str = _true_colors['SAPPHIRE']
    SAPPHIRE_BLUE: str = _true_colors['SAPPHIRE_BLUE']
    SAPPHIRE_CRAYOLA: str = _true_colors['SAPPHIRE_CRAYOLA']
    SATIN_SHEEN_GOLD: str = _true_colors['SATIN_SHEEN_GOLD']
    SCARLET: str = _true_colors['SCARLET']
    SCHAUSS_PINK: str = _true_colors['SCHAUSS_PINK']
    SCHOOL_BUS_YELLOW: str = _true_colors['SCHOOL_BUS_YELLOW']
    SCREAMIN_GREEN: str = _true_colors['SCREAMIN_GREEN']
    SEA_GREEN: str = _true_colors['SEA_GREEN']
    SEA_GREEN_CRAYOLA: str = _true_colors['SEA_GREEN_CRAYOLA']
    SEANCE: str = _true_colors['SEANCE']
    SEAL_BROWN: str = _true_colors['SEAL_BROWN']
    SEASHELL: str = _true_colors['SEASHELL']
    SECRET: str = _true_colors['SECRET']
    SELECTIVE_YELLOW: str = _true_colors['SELECTIVE_YELLOW']
    SEPIA: str = _true_colors['SEPIA']
    SHADOW: str = _true_colors['SHADOW']
    SHADOW_BLUE: str = _true_colors['SHADOW_BLUE']
    SHAMROCK_GREEN: str = _true_colors['SHAMROCK_GREEN']
    SHEEN_GREEN: str = _true_colors['SHEEN_GREEN']
    SHIMMERING_BLUSH: str = _true_colors['SHIMMERING_BLUSH']
    SHINY_SHAMROCK: str = _true_colors['SHINY_SHAMROCK']
    SHOCKING_PINK: str = _true_colors['SHOCKING_PINK']
    SHOCKING_PINK_CRAYOLA: str = _true_colors['SHOCKING_PINK_CRAYOLA']
    SIENNA: str = _true_colors['SIENNA']
    SILVER: str = _true_colors['SILVER']
    SILVER_CRAYOLA: str = _true_colors['SILVER_CRAYOLA']
    SILVER_METALLIC: str = _true_colors['SILVER_METALLIC']
    SILVER_CHALICE: str = _true_colors['SILVER_CHALICE']
    SILVER_PINK: str = _true_colors['SILVER_PINK']
    SILVER_SAND: str = _true_colors['SILVER_SAND']
    SINOPIA: str = _true_colors['SINOPIA']
    SIZZLING_RED: str = _true_colors['SIZZLING_RED']
    SIZZLING_SUNRISE: str = _true_colors['SIZZLING_SUNRISE']
    SKOBELOFF: str = _true_colors['SKOBELOFF']
    SKY_BLUE: str = _true_colors['SKY_BLUE']
    SKY_BLUE_CRAYOLA: str = _true_colors['SKY_BLUE_CRAYOLA']
    SKY_MAGENTA: str = _true_colors['SKY_MAGENTA']
    SLATE_BLUE: str = _true_colors['SLATE_BLUE']
    SLATE_GRAY: str = _true_colors['SLATE_GRAY']
    SLIMY_GREEN: str = _true_colors['SLIMY_GREEN']
    SMITTEN: str = _true_colors['SMITTEN']
    SMOKY_BLACK: str = _true_colors['SMOKY_BLACK']
    SNOW: str = _true_colors['SNOW']
    SOLID_PINK: str = _true_colors['SOLID_PINK']
    SONIC_SILVER: str = _true_colors['SONIC_SILVER']
    SPACE_CADET: str = _true_colors['SPACE_CADET']
    SPANISH_BISTRE: str = _true_colors['SPANISH_BISTRE']
    SPANISH_BLUE: str = _true_colors['SPANISH_BLUE']
    SPANISH_CARMINE: str = _true_colors['SPANISH_CARMINE']
    SPANISH_GRAY: str = _true_colors['SPANISH_GRAY']
    SPANISH_GREEN: str = _true_colors['SPANISH_GREEN']
    SPANISH_ORANGE: str = _true_colors['SPANISH_ORANGE']
    SPANISH_PINK: str = _true_colors['SPANISH_PINK']
    SPANISH_RED: str = _true_colors['SPANISH_RED']
    SPANISH_SKY_BLUE: str = _true_colors['SPANISH_SKY_BLUE']
    SPANISH_VIOLET: str = _true_colors['SPANISH_VIOLET']
    SPANISH_VIRIDIAN: str = _true_colors['SPANISH_VIRIDIAN']
    SPRING_BUD: str = _true_colors['SPRING_BUD']
    SPRING_FROST: str = _true_colors['SPRING_FROST']
    SPRING_GREEN: str = _true_colors['SPRING_GREEN']
    SPRING_GREEN_CRAYOLA: str = _true_colors['SPRING_GREEN_CRAYOLA']
    STAR_COMMAND_BLUE: str = _true_colors['STAR_COMMAND_BLUE']
    STEEL_BLUE: str = _true_colors['STEEL_BLUE']
    STEEL_PINK: str = _true_colors['STEEL_PINK']
    STIL_DE_GRAIN_YELLOW: str = _true_colors['STIL_DE_GRAIN_YELLOW']
    STIZZA: str = _true_colors['STIZZA']
    STRAW: str = _true_colors['STRAW']
    STRAWBERRY: str = _true_colors['STRAWBERRY']
    STRAWBERRY_BLONDE: str = _true_colors['STRAWBERRY_BLONDE']
    STRONG_LIME_GREEN: str = _true_colors['STRONG_LIME_GREEN']
    SUGAR_PLUM: str = _true_colors['SUGAR_PLUM']
    SUNGLOW: str = _true_colors['SUNGLOW']
    SUNRAY: str = _true_colors['SUNRAY']
    SUNSET: str = _true_colors['SUNSET']
    SUPER_PINK: str = _true_colors['SUPER_PINK']
    SWEET_BROWN: str = _true_colors['SWEET_BROWN']
    SYRACUSE_ORANGE: str = _true_colors['SYRACUSE_ORANGE']
    TAN: str = _true_colors['TAN']
    TAN_CRAYOLA: str = _true_colors['TAN_CRAYOLA']
    TANGERINE: str = _true_colors['TANGERINE']
    TANGO_PINK: str = _true_colors['TANGO_PINK']
    TART_ORANGE: str = _true_colors['TART_ORANGE']
    TAUPE: str = _true_colors['TAUPE']
    TAUPE_GRAY: str = _true_colors['TAUPE_GRAY']
    TEA_GREEN: str = _true_colors['TEA_GREEN']
    TEA_ROSE: str = _true_colors['TEA_ROSE']
    TEAL: str = _true_colors['TEAL']
    TEAL_BLUE: str = _true_colors['TEAL_BLUE']
    TECHNOBOTANICA: str = _true_colors['TECHNOBOTANICA']
    TELEMAGENTA: str = _true_colors['TELEMAGENTA']
    TENNE_TAWNY: str = _true_colors['TENNE_TAWNY']
    TERRA_COTTA: str = _true_colors['TERRA_COTTA']
    THISTLE: str = _true_colors['THISTLE']
    THULIAN_PINK: str = _true_colors['THULIAN_PINK']
    TICKLE_ME_PINK: str = _true_colors['TICKLE_ME_PINK']
    TIFFANY_BLUE: str = _true_colors['TIFFANY_BLUE']
    TIMBERWOLF: str = _true_colors['TIMBERWOLF']
    TITANIUM_YELLOW: str = _true_colors['TITANIUM_YELLOW']
    TOMATO: str = _true_colors['TOMATO']
    TOURMALINE: str = _true_colors['TOURMALINE']
    TROPICAL_RAINFOREST: str = _true_colors['TROPICAL_RAINFOREST']
    TRUE_BLUE: str = _true_colors['TRUE_BLUE']
    TRYPAN_BLUE: str = _true_colors['TRYPAN_BLUE']
    TUFTS_BLUE: str = _true_colors['TUFTS_BLUE']
    TUMBLEWEED: str = _true_colors['TUMBLEWEED']
    TURQUOISE: str = _true_colors['TURQUOISE']
    TURQUOISE_BLUE: str = _true_colors['TURQUOISE_BLUE']
    TURQUOISE_GREEN: str = _true_colors['TURQUOISE_GREEN']
    TURTLE_GREEN: str = _true_colors['TURTLE_GREEN']
    TUSCAN: str = _true_colors['TUSCAN']
    TUSCAN_BROWN: str = _true_colors['TUSCAN_BROWN']
    TUSCAN_RED: str = _true_colors['TUSCAN_RED']
    TUSCAN_TAN: str = _true_colors['TUSCAN_TAN']
    TUSCANY: str = _true_colors['TUSCANY']
    TWILIGHT_LAVENDER: str = _true_colors['TWILIGHT_LAVENDER']
    TYRIAN_PURPLE: str = _true_colors['TYRIAN_PURPLE']
    UA_BLUE: str = _true_colors['UA_BLUE']
    UA_RED: str = _true_colors['UA_RED']
    ULTRAMARINE: str = _true_colors['ULTRAMARINE']
    ULTRAMARINE_BLUE: str = _true_colors['ULTRAMARINE_BLUE']
    ULTRA_PINK: str = _true_colors['ULTRA_PINK']
    ULTRA_RED: str = _true_colors['ULTRA_RED']
    UMBER: str = _true_colors['UMBER']
    UNBLEACHED_SILK: str = _true_colors['UNBLEACHED_SILK']
    UNITED_NATIONS_BLUE: str = _true_colors['UNITED_NATIONS_BLUE']
    UNIVERSITY_OF_PENNSYLVANIA_RED: str = _true_colors['UNIVERSITY_OF_PENNSYLVANIA_RED']
    UNMELLOW_YELLOW: str = _true_colors['UNMELLOW_YELLOW']
    UP_FOREST_GREEN: str = _true_colors['UP_FOREST_GREEN']
    UP_MAROON: str = _true_colors['UP_MAROON']
    UPSDELL_RED: str = _true_colors['UPSDELL_RED']
    URANIAN_BLUE: str = _true_colors['URANIAN_BLUE']
    USAFA_BLUE: str = _true_colors['USAFA_BLUE']
    VAN_DYKE_BROWN: str = _true_colors['VAN_DYKE_BROWN']
    VANILLA: str = _true_colors['VANILLA']
    VANILLA_ICE: str = _true_colors['VANILLA_ICE']
    VEGAS_GOLD: str = _true_colors['VEGAS_GOLD']
    VENETIAN_RED: str = _true_colors['VENETIAN_RED']
    VERDIGRIS: str = _true_colors['VERDIGRIS']
    VERMILION: str = _true_colors['VERMILION']
    VERONICA: str = _true_colors['VERONICA']
    VIOLET: str = _true_colors['VIOLET']
    VIOLET_COLOR_WHEEL: str = _true_colors['VIOLET_COLOR_WHEEL']
    VIOLET_CRAYOLA: str = _true_colors['VIOLET_CRAYOLA']
    VIOLET_RYB: str = _true_colors['VIOLET_RYB']
    VIOLET_WEB: str = _true_colors['VIOLET_WEB']
    VIOLET_BLUE: str = _true_colors['VIOLET_BLUE']
    VIOLET_BLUE_CRAYOLA: str = _true_colors['VIOLET_BLUE_CRAYOLA']
    VIOLET_RED: str = _true_colors['VIOLET_RED']
    VIOLET_REDPERBANG: str = _true_colors['VIOLET_REDPERBANG']
    VIRIDIAN: str = _true_colors['VIRIDIAN']
    VIRIDIAN_GREEN: str = _true_colors['VIRIDIAN_GREEN']
    VIVID_BURGUNDY: str = _true_colors['VIVID_BURGUNDY']
    VIVID_SKY_BLUE: str = _true_colors['VIVID_SKY_BLUE']
    VIVID_TANGERINE: str = _true_colors['VIVID_TANGERINE']
    VIVID_VIOLET: str = _true_colors['VIVID_VIOLET']
    VOLT: str = _true_colors['VOLT']
    WARM_BLACK: str = _true_colors['WARM_BLACK']
    WEEZY_BLUE: str = _true_colors['WEEZY_BLUE']
    WHEAT: str = _true_colors['WHEAT']
    WILD_BLUE_YONDER: str = _true_colors['WILD_BLUE_YONDER']
    WILD_ORCHID: str = _true_colors['WILD_ORCHID']
    WILD_STRAWBERRY: str = _true_colors['WILD_STRAWBERRY']
    WILD_WATERMELON: str = _true_colors['WILD_WATERMELON']
    WINDSOR_TAN: str = _true_colors['WINDSOR_TAN']
    WINE: str = _true_colors['WINE']
    WINE_DREGS: str = _true_colors['WINE_DREGS']
    WINTER_SKY: str = _true_colors['WINTER_SKY']
    WINTERGREEN_DREAM: str = _true_colors['WINTERGREEN_DREAM']
    WISTERIA: str = _true_colors['WISTERIA']
    WOOD_BROWN: str = _true_colors['WOOD_BROWN']
    XANADU: str = _true_colors['XANADU']
    XANTHIC: str = _true_colors['XANTHIC']
    XANTHOUS: str = _true_colors['XANTHOUS']
    YALE_BLUE: str = _true_colors['YALE_BLUE']
    YELLOW_CRAYOLA: str = _true_colors['YELLOW_CRAYOLA']
    YELLOW_MUNSELL: str = _true_colors['YELLOW_MUNSELL']
    YELLOW_NCS: str = _true_colors['YELLOW_NCS']
    YELLOW_PANTONE: str = _true_colors['YELLOW_PANTONE']
    YELLOW_PROCESS: str = _true_colors['YELLOW_PROCESS']
    YELLOW_RYB: str = _true_colors['YELLOW_RYB']
    YELLOW_GREEN: str = _true_colors['YELLOW_GREEN']
    YELLOW_GREEN_CRAYOLA: str = _true_colors['YELLOW_GREEN_CRAYOLA']
    YELLOW_GREEN_COLOR_WHEEL: str = _true_colors['YELLOW_GREEN_COLOR_WHEEL']
    YELLOW_ORANGE: str = _true_colors['YELLOW_ORANGE']
    YELLOW_ORANGE_COLOR_WHEEL: str = _true_colors['YELLOW_ORANGE_COLOR_WHEEL']
    YELLOW_SUNSHINE: str = _true_colors['YELLOW_SUNSHINE']
    YINMN_BLUE: str = _true_colors['YINMN_BLUE']
    ZAFFRE: str = _true_colors['ZAFFRE']
    ZINNWALDITE_BROWN: str = _true_colors['ZINNWALDITE_BROWN']
    ZOMP: str = _true_colors['ZOMP']

    @classmethod
    def add_color(cls, name: str, ansi_code: str, true_color: Optional[bool] = True) -> None:
        """
        Enables the addition of a custom background color to the dictionary, supporting both standard
        and true color formats. However, it's essential to note that true colors can only be added if
        the terminal supports them.
        :param name: The name for the custom background color.
        :type name: str
        :param ansi_code: The ANSI code color value for the custom background.
        :type ansi_code: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(ansi_code, str, 'ansi_code should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')
        Validate.validate_ansi(ansi_code)

        if true_color and not is_true_color_supported():
            raise Warning('True colors are not supported by this terminal.')

        code = ansi_code[2:].rstrip('m')
        if true_color:
            pattern = (
                rf'^{Layer.Background.value};2;'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5]);'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5]);'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5])$'
            )
            if not re.match(pattern, code):
                raise ValueError('Unsupported ANSI code format.')

            cls._true_colors[name.upper()] = ansi_code
        else:
            if not code.isdigit():
                raise ValueError('Unsupported ANSI code format.')

            cls._standard_colors[name.upper()] = ansi_code

    @classmethod
    def get_colors(cls, true_color: Optional[bool] = True) -> dict:
        """
        Generates a dictionary containing a list of all colors based on the provided input.
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The dictionary containing the list of colors based on the provided input.
        :rtype: dict
        """
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            return dict(sorted(cls._true_colors.items()))
        else:
            return dict(sorted(cls._standard_colors.items()))

    @classmethod
    def get_color(cls, name: str, true_color: Optional[bool] = True) -> str:
        """
        Obtains the color code corresponding to the provided input.
        :param name: The name of the color to retrieve.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The color code value of the provided color name.
        :rtype: str
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            result = cls._true_colors.get(name.upper())
        else:
            result = cls._standard_colors.get(name.upper())

        if result is None:
            raise ValueError(
                f'{name} is not a valid {"true" if true_color else "standard"} '
                f'color value for TextBackgroundColor'
            )

        return result

    @classmethod
    def is_standard_color(cls, name: str) -> bool:
        """
        Checks whether the provided color name corresponds to a standard color.
        :param name: The name of the color to be validated.
        :type name: str
        :return: True if the provided color is a standard color, False otherwise.
        :rtype: bool
        """
        return cls.is_valid_color(name, true_color=False)

    @classmethod
    def is_true_color(cls, name: str) -> bool:
        """
        Checks whether the provided color name corresponds to a true color.
        :param name: The name of the color to be validated.
        :type name: str
        :return: True if the provided color is a true color, False otherwise.
        :rtype: bool
        """
        return cls.is_valid_color(name, true_color=True)

    @classmethod
    def is_valid_color(cls, name: str, true_color: Optional[bool] = True) -> bool:
        """
        Checks whether the provided color name corresponds to either a standard or true color.
        :param name: The name of the color to be validated.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :return: True if the provided color is either a standard or true color, False otherwise.
        :rtype: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        try:
            return cls.get_color(name, true_color) is not None
        except ValueError:
            return False

    @classmethod
    def remove_color(cls, name: str, true_color: Optional[bool] = True) -> None:
        """
        Deletes the custom background color specified by name from the dictionary.
        :param name: The name of the color to be removed.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            if name.upper() in cls._true_colors:
                del cls._true_colors[name.upper()]
        else:
            if name.upper() in cls._standard_colors:
                del cls._standard_colors[name.upper()]


class TextColor:
    """
    This class defines text foreground colors for styling console text within the terminal.
    It includes both standard and true colors. The true colors are sourced from Wikipedia;
    please refer to the licensing information for more details. Additionally, the class offers
    methods to handle custom colors.
    """

    # Standard terminal colors supported by various operating systems
    _standard_colors = {
        'BLACK': "\033[30m",
        'RED': "\033[31m",
        'GREEN': "\033[32m",
        'YELLOW': "\033[33m",
        'BLUE': "\033[34m",
        'MAGENTA': "\033[35m",
        'CYAN': "\033[36m",
        'WHITE': "\033[37m"
    }

    # True colors, also known as 24-bit color, allow for a much broader range of colors than the
    # traditional 8-bit color systems. They enable millions of distinct colors to be displayed,
    # providing more accurate and vibrant representations of images and graphics. However, support
    # for true colors may vary depending on the capabilities of the terminal and the underlying operating system.
    _true_colors = {
        'ABSOLUTE_ZERO': Color.hex_to_ansi(HEXCodes.ABSOLUTE_ZERO, Layer.Foreground),
        'ACID_GREEN': Color.hex_to_ansi(HEXCodes.ACID_GREEN, Layer.Foreground),
        'AERO': Color.hex_to_ansi(HEXCodes.AERO, Layer.Foreground),
        'AFRICAN_VIOLET': Color.hex_to_ansi(HEXCodes.AFRICAN_VIOLET, Layer.Foreground),
        'AIR_SUPERIORITY_BLUE': Color.hex_to_ansi(HEXCodes.AIR_SUPERIORITY_BLUE, Layer.Foreground),
        'ALICE_BLUE': Color.hex_to_ansi(HEXCodes.ALICE_BLUE, Layer.Foreground),
        'ALIZARIN': Color.hex_to_ansi(HEXCodes.ALIZARIN, Layer.Foreground),
        'ALLOY_ORANGE': Color.hex_to_ansi(HEXCodes.ALLOY_ORANGE, Layer.Foreground),
        'ALMOND': Color.hex_to_ansi(HEXCodes.ALMOND, Layer.Foreground),
        'AMARANTH_DEEP_PURPLE': Color.hex_to_ansi(HEXCodes.AMARANTH_DEEP_PURPLE, Layer.Foreground),
        'AMARANTH_PINK': Color.hex_to_ansi(HEXCodes.AMARANTH_PINK, Layer.Foreground),
        'AMARANTH_PURPLE': Color.hex_to_ansi(HEXCodes.AMARANTH_PURPLE, Layer.Foreground),
        'AMAZON': Color.hex_to_ansi(HEXCodes.AMAZON, Layer.Foreground),
        'AMBER': Color.hex_to_ansi(HEXCodes.AMBER, Layer.Foreground),
        'AMETHYST': Color.hex_to_ansi(HEXCodes.AMETHYST, Layer.Foreground),
        'ANDROID_GREEN': Color.hex_to_ansi(HEXCodes.ANDROID_GREEN, Layer.Foreground),
        'ANTIQUE_BRASS': Color.hex_to_ansi(HEXCodes.ANTIQUE_BRASS, Layer.Foreground),
        'ANTIQUE_BRONZE': Color.hex_to_ansi(HEXCodes.ANTIQUE_BRONZE, Layer.Foreground),
        'ANTIQUE_FUCHSIA': Color.hex_to_ansi(HEXCodes.ANTIQUE_FUCHSIA, Layer.Foreground),
        'ANTIQUE_RUBY': Color.hex_to_ansi(HEXCodes.ANTIQUE_RUBY, Layer.Foreground),
        'ANTIQUE_WHITE': Color.hex_to_ansi(HEXCodes.ANTIQUE_WHITE, Layer.Foreground),
        'APRICOT': Color.hex_to_ansi(HEXCodes.APRICOT, Layer.Foreground),
        'AQUA': Color.hex_to_ansi(HEXCodes.AQUA, Layer.Foreground),
        'AQUAMARINE': Color.hex_to_ansi(HEXCodes.AQUAMARINE, Layer.Foreground),
        'ARCTIC_LIME': Color.hex_to_ansi(HEXCodes.ARCTIC_LIME, Layer.Foreground),
        'ARTICHOKE_GREEN': Color.hex_to_ansi(HEXCodes.ARTICHOKE_GREEN, Layer.Foreground),
        'ARYLIDE_YELLOW': Color.hex_to_ansi(HEXCodes.ARYLIDE_YELLOW, Layer.Foreground),
        'ASH_GRAY': Color.hex_to_ansi(HEXCodes.ASH_GRAY, Layer.Foreground),
        'ATOMIC_TANGERINE': Color.hex_to_ansi(HEXCodes.ATOMIC_TANGERINE, Layer.Foreground),
        'AUREOLIN': Color.hex_to_ansi(HEXCodes.AUREOLIN, Layer.Foreground),
        'AZURE': Color.hex_to_ansi(HEXCodes.AZURE, Layer.Foreground),
        'BABY_BLUE': Color.hex_to_ansi(HEXCodes.BABY_BLUE, Layer.Foreground),
        'BABY_BLUE_EYES': Color.hex_to_ansi(HEXCodes.BABY_BLUE_EYES, Layer.Foreground),
        'BABY_PINK': Color.hex_to_ansi(HEXCodes.BABY_PINK, Layer.Foreground),
        'BABY_POWDER': Color.hex_to_ansi(HEXCodes.BABY_POWDER, Layer.Foreground),
        'BAKER_MILLER_PINK': Color.hex_to_ansi(HEXCodes.BAKER_MILLER_PINK, Layer.Foreground),
        'BANANA_MANIA': Color.hex_to_ansi(HEXCodes.BANANA_MANIA, Layer.Foreground),
        'BARBIE_PINK': Color.hex_to_ansi(HEXCodes.BARBIE_PINK, Layer.Foreground),
        'BARN_RED': Color.hex_to_ansi(HEXCodes.BARN_RED, Layer.Foreground),
        'BATTLESHIP_GREY': Color.hex_to_ansi(HEXCodes.BATTLESHIP_GREY, Layer.Foreground),
        'BEAU_BLUE': Color.hex_to_ansi(HEXCodes.BEAU_BLUE, Layer.Foreground),
        'BEAVER': Color.hex_to_ansi(HEXCodes.BEAVER, Layer.Foreground),
        'BEIGE': Color.hex_to_ansi(HEXCodes.BEIGE, Layer.Foreground),
        'B_DAZZLED_BLUE': Color.hex_to_ansi(HEXCodes.B_DAZZLED_BLUE, Layer.Foreground),
        'BIG_DIP_O_RUBY': Color.hex_to_ansi(HEXCodes.BIG_DIP_O_RUBY, Layer.Foreground),
        'BISQUE': Color.hex_to_ansi(HEXCodes.BISQUE, Layer.Foreground),
        'BISTRE': Color.hex_to_ansi(HEXCodes.BISTRE, Layer.Foreground),
        'BISTRE_BROWN': Color.hex_to_ansi(HEXCodes.BISTRE_BROWN, Layer.Foreground),
        'BITTER_LEMON': Color.hex_to_ansi(HEXCodes.BITTER_LEMON, Layer.Foreground),
        'BLACK_BEAN': Color.hex_to_ansi(HEXCodes.BLACK_BEAN, Layer.Foreground),
        'BLACK_CORAL': Color.hex_to_ansi(HEXCodes.BLACK_CORAL, Layer.Foreground),
        'BLACK_OLIVE': Color.hex_to_ansi(HEXCodes.BLACK_OLIVE, Layer.Foreground),
        'BLACK_SHADOWS': Color.hex_to_ansi(HEXCodes.BLACK_SHADOWS, Layer.Foreground),
        'BLANCHED_ALMOND': Color.hex_to_ansi(HEXCodes.BLANCHED_ALMOND, Layer.Foreground),
        'BLAST_OFF_BRONZE': Color.hex_to_ansi(HEXCodes.BLAST_OFF_BRONZE, Layer.Foreground),
        'BLEU_DE_FRANCE': Color.hex_to_ansi(HEXCodes.BLEU_DE_FRANCE, Layer.Foreground),
        'BLIZZARD_BLUE': Color.hex_to_ansi(HEXCodes.BLIZZARD_BLUE, Layer.Foreground),
        'BLOOD_RED': Color.hex_to_ansi(HEXCodes.BLOOD_RED, Layer.Foreground),
        'BLUE_CRAYOLA': Color.hex_to_ansi(HEXCodes.BLUE_CRAYOLA, Layer.Foreground),
        'BLUE_MUNSELL': Color.hex_to_ansi(HEXCodes.BLUE_MUNSELL, Layer.Foreground),
        'BLUE_NCS': Color.hex_to_ansi(HEXCodes.BLUE_NCS, Layer.Foreground),
        'BLUE_PANTONE': Color.hex_to_ansi(HEXCodes.BLUE_PANTONE, Layer.Foreground),
        'BLUE_PIGMENT': Color.hex_to_ansi(HEXCodes.BLUE_PIGMENT, Layer.Foreground),
        'BLUE_BELL': Color.hex_to_ansi(HEXCodes.BLUE_BELL, Layer.Foreground),
        'BLUE_GRAY_CRAYOLA': Color.hex_to_ansi(HEXCodes.BLUE_GRAY_CRAYOLA, Layer.Foreground),
        'BLUE_JEANS': Color.hex_to_ansi(HEXCodes.BLUE_JEANS, Layer.Foreground),
        'BLUE_SAPPHIRE': Color.hex_to_ansi(HEXCodes.BLUE_SAPPHIRE, Layer.Foreground),
        'BLUE_VIOLET': Color.hex_to_ansi(HEXCodes.BLUE_VIOLET, Layer.Foreground),
        'BLUE_YONDER': Color.hex_to_ansi(HEXCodes.BLUE_YONDER, Layer.Foreground),
        'BLUETIFUL': Color.hex_to_ansi(HEXCodes.BLUETIFUL, Layer.Foreground),
        'BLUSH': Color.hex_to_ansi(HEXCodes.BLUSH, Layer.Foreground),
        'BOLE': Color.hex_to_ansi(HEXCodes.BOLE, Layer.Foreground),
        'BONE': Color.hex_to_ansi(HEXCodes.BONE, Layer.Foreground),
        'BRICK_RED': Color.hex_to_ansi(HEXCodes.BRICK_RED, Layer.Foreground),
        'BRIGHT_LILAC': Color.hex_to_ansi(HEXCodes.BRIGHT_LILAC, Layer.Foreground),
        'BRIGHT_YELLOW_CRAYOLA': Color.hex_to_ansi(HEXCodes.BRIGHT_YELLOW_CRAYOLA, Layer.Foreground),
        'BRITISH_RACING_GREEN': Color.hex_to_ansi(HEXCodes.BRITISH_RACING_GREEN, Layer.Foreground),
        'BRONZE': Color.hex_to_ansi(HEXCodes.BRONZE, Layer.Foreground),
        'BROWN': Color.hex_to_ansi(HEXCodes.BROWN, Layer.Foreground),
        'BROWN_SUGAR': Color.hex_to_ansi(HEXCodes.BROWN_SUGAR, Layer.Foreground),
        'BUD_GREEN': Color.hex_to_ansi(HEXCodes.BUD_GREEN, Layer.Foreground),
        'BUFF': Color.hex_to_ansi(HEXCodes.BUFF, Layer.Foreground),
        'BURGUNDY': Color.hex_to_ansi(HEXCodes.BURGUNDY, Layer.Foreground),
        'BURLYWOOD': Color.hex_to_ansi(HEXCodes.BURLYWOOD, Layer.Foreground),
        'BURNISHED_BROWN': Color.hex_to_ansi(HEXCodes.BURNISHED_BROWN, Layer.Foreground),
        'BURNT_ORANGE': Color.hex_to_ansi(HEXCodes.BURNT_ORANGE, Layer.Foreground),
        'BURNT_SIENNA': Color.hex_to_ansi(HEXCodes.BURNT_SIENNA, Layer.Foreground),
        'BURNT_UMBER': Color.hex_to_ansi(HEXCodes.BURNT_UMBER, Layer.Foreground),
        'BYZANTINE': Color.hex_to_ansi(HEXCodes.BYZANTINE, Layer.Foreground),
        'BYZANTIUM': Color.hex_to_ansi(HEXCodes.BYZANTIUM, Layer.Foreground),
        'CADET_BLUE': Color.hex_to_ansi(HEXCodes.CADET_BLUE, Layer.Foreground),
        'CADET_GREY': Color.hex_to_ansi(HEXCodes.CADET_GREY, Layer.Foreground),
        'CADMIUM_GREEN': Color.hex_to_ansi(HEXCodes.CADMIUM_GREEN, Layer.Foreground),
        'CADMIUM_ORANGE': Color.hex_to_ansi(HEXCodes.CADMIUM_ORANGE, Layer.Foreground),
        'CAFE_AU_LAIT': Color.hex_to_ansi(HEXCodes.CAFE_AU_LAIT, Layer.Foreground),
        'CAFE_NOIR': Color.hex_to_ansi(HEXCodes.CAFE_NOIR, Layer.Foreground),
        'CAMBRIDGE_BLUE': Color.hex_to_ansi(HEXCodes.CAMBRIDGE_BLUE, Layer.Foreground),
        'CAMEL': Color.hex_to_ansi(HEXCodes.CAMEL, Layer.Foreground),
        'CAMEO_PINK': Color.hex_to_ansi(HEXCodes.CAMEO_PINK, Layer.Foreground),
        'CANARY': Color.hex_to_ansi(HEXCodes.CANARY, Layer.Foreground),
        'CANARY_YELLOW': Color.hex_to_ansi(HEXCodes.CANARY_YELLOW, Layer.Foreground),
        'CANDY_PINK': Color.hex_to_ansi(HEXCodes.CANDY_PINK, Layer.Foreground),
        'CARDINAL': Color.hex_to_ansi(HEXCodes.CARDINAL, Layer.Foreground),
        'CARIBBEAN_GREEN': Color.hex_to_ansi(HEXCodes.CARIBBEAN_GREEN, Layer.Foreground),
        'CARMINE': Color.hex_to_ansi(HEXCodes.CARMINE, Layer.Foreground),
        'CARMINE_M_P': Color.hex_to_ansi(HEXCodes.CARMINE_M_P, Layer.Foreground),
        'CARNATION_PINK': Color.hex_to_ansi(HEXCodes.CARNATION_PINK, Layer.Foreground),
        'CARNELIAN': Color.hex_to_ansi(HEXCodes.CARNELIAN, Layer.Foreground),
        'CAROLINA_BLUE': Color.hex_to_ansi(HEXCodes.CAROLINA_BLUE, Layer.Foreground),
        'CARROT_ORANGE': Color.hex_to_ansi(HEXCodes.CARROT_ORANGE, Layer.Foreground),
        'CATAWBA': Color.hex_to_ansi(HEXCodes.CATAWBA, Layer.Foreground),
        'CEDAR_CHEST': Color.hex_to_ansi(HEXCodes.CEDAR_CHEST, Layer.Foreground),
        'CELADON': Color.hex_to_ansi(HEXCodes.CELADON, Layer.Foreground),
        'CELESTE': Color.hex_to_ansi(HEXCodes.CELESTE, Layer.Foreground),
        'CERISE': Color.hex_to_ansi(HEXCodes.CERISE, Layer.Foreground),
        'CERULEAN': Color.hex_to_ansi(HEXCodes.CERULEAN, Layer.Foreground),
        'CERULEAN_BLUE': Color.hex_to_ansi(HEXCodes.CERULEAN_BLUE, Layer.Foreground),
        'CERULEAN_FROST': Color.hex_to_ansi(HEXCodes.CERULEAN_FROST, Layer.Foreground),
        'CERULEAN_CRAYOLA': Color.hex_to_ansi(HEXCodes.CERULEAN_CRAYOLA, Layer.Foreground),
        'CERULEAN_RGB': Color.hex_to_ansi(HEXCodes.CERULEAN_RGB, Layer.Foreground),
        'CHAMPAGNE': Color.hex_to_ansi(HEXCodes.CHAMPAGNE, Layer.Foreground),
        'CHAMPAGNE_PINK': Color.hex_to_ansi(HEXCodes.CHAMPAGNE_PINK, Layer.Foreground),
        'CHARCOAL': Color.hex_to_ansi(HEXCodes.CHARCOAL, Layer.Foreground),
        'CHARM_PINK': Color.hex_to_ansi(HEXCodes.CHARM_PINK, Layer.Foreground),
        'CHARTREUSE_WEB': Color.hex_to_ansi(HEXCodes.CHARTREUSE_WEB, Layer.Foreground),
        'CHERRY_BLOSSOM_PINK': Color.hex_to_ansi(HEXCodes.CHERRY_BLOSSOM_PINK, Layer.Foreground),
        'CHESTNUT': Color.hex_to_ansi(HEXCodes.CHESTNUT, Layer.Foreground),
        'CHILI_RED': Color.hex_to_ansi(HEXCodes.CHILI_RED, Layer.Foreground),
        'CHINA_PINK': Color.hex_to_ansi(HEXCodes.CHINA_PINK, Layer.Foreground),
        'CHINESE_RED': Color.hex_to_ansi(HEXCodes.CHINESE_RED, Layer.Foreground),
        'CHINESE_VIOLET': Color.hex_to_ansi(HEXCodes.CHINESE_VIOLET, Layer.Foreground),
        'CHINESE_YELLOW': Color.hex_to_ansi(HEXCodes.CHINESE_YELLOW, Layer.Foreground),
        'CHOCOLATE_TRADITIONAL': Color.hex_to_ansi(HEXCodes.CHOCOLATE_TRADITIONAL, Layer.Foreground),
        'CHOCOLATE_WEB': Color.hex_to_ansi(HEXCodes.CHOCOLATE_WEB, Layer.Foreground),
        'CINEREOUS': Color.hex_to_ansi(HEXCodes.CINEREOUS, Layer.Foreground),
        'CINNABAR': Color.hex_to_ansi(HEXCodes.CINNABAR, Layer.Foreground),
        'CINNAMON_SATIN': Color.hex_to_ansi(HEXCodes.CINNAMON_SATIN, Layer.Foreground),
        'CITRINE': Color.hex_to_ansi(HEXCodes.CITRINE, Layer.Foreground),
        'CITRON': Color.hex_to_ansi(HEXCodes.CITRON, Layer.Foreground),
        'CLARET': Color.hex_to_ansi(HEXCodes.CLARET, Layer.Foreground),
        'COFFEE': Color.hex_to_ansi(HEXCodes.COFFEE, Layer.Foreground),
        'COLUMBIA_BLUE': Color.hex_to_ansi(HEXCodes.COLUMBIA_BLUE, Layer.Foreground),
        'CONGO_PINK': Color.hex_to_ansi(HEXCodes.CONGO_PINK, Layer.Foreground),
        'COOL_GREY': Color.hex_to_ansi(HEXCodes.COOL_GREY, Layer.Foreground),
        'COPPER': Color.hex_to_ansi(HEXCodes.COPPER, Layer.Foreground),
        'COPPER_CRAYOLA': Color.hex_to_ansi(HEXCodes.COPPER_CRAYOLA, Layer.Foreground),
        'COPPER_PENNY': Color.hex_to_ansi(HEXCodes.COPPER_PENNY, Layer.Foreground),
        'COPPER_RED': Color.hex_to_ansi(HEXCodes.COPPER_RED, Layer.Foreground),
        'COPPER_ROSE': Color.hex_to_ansi(HEXCodes.COPPER_ROSE, Layer.Foreground),
        'COQUELICOT': Color.hex_to_ansi(HEXCodes.COQUELICOT, Layer.Foreground),
        'CORAL': Color.hex_to_ansi(HEXCodes.CORAL, Layer.Foreground),
        'CORAL_PINK': Color.hex_to_ansi(HEXCodes.CORAL_PINK, Layer.Foreground),
        'CORDOVAN': Color.hex_to_ansi(HEXCodes.CORDOVAN, Layer.Foreground),
        'CORN': Color.hex_to_ansi(HEXCodes.CORN, Layer.Foreground),
        'CORNFLOWER_BLUE': Color.hex_to_ansi(HEXCodes.CORNFLOWER_BLUE, Layer.Foreground),
        'CORNSILK': Color.hex_to_ansi(HEXCodes.CORNSILK, Layer.Foreground),
        'COSMIC_COBALT': Color.hex_to_ansi(HEXCodes.COSMIC_COBALT, Layer.Foreground),
        'COSMIC_LATTE': Color.hex_to_ansi(HEXCodes.COSMIC_LATTE, Layer.Foreground),
        'COYOTE_BROWN': Color.hex_to_ansi(HEXCodes.COYOTE_BROWN, Layer.Foreground),
        'COTTON_CANDY': Color.hex_to_ansi(HEXCodes.COTTON_CANDY, Layer.Foreground),
        'CREAM': Color.hex_to_ansi(HEXCodes.CREAM, Layer.Foreground),
        'CRIMSON': Color.hex_to_ansi(HEXCodes.CRIMSON, Layer.Foreground),
        'CRIMSON_UA': Color.hex_to_ansi(HEXCodes.CRIMSON_UA, Layer.Foreground),
        'CULTURED_PEARL': Color.hex_to_ansi(HEXCodes.CULTURED_PEARL, Layer.Foreground),
        'CYAN_PROCESS': Color.hex_to_ansi(HEXCodes.CYAN_PROCESS, Layer.Foreground),
        'CYBER_GRAPE': Color.hex_to_ansi(HEXCodes.CYBER_GRAPE, Layer.Foreground),
        'CYBER_YELLOW': Color.hex_to_ansi(HEXCodes.CYBER_YELLOW, Layer.Foreground),
        'CYCLAMEN': Color.hex_to_ansi(HEXCodes.CYCLAMEN, Layer.Foreground),
        'DANDELION': Color.hex_to_ansi(HEXCodes.DANDELION, Layer.Foreground),
        'DARK_BROWN': Color.hex_to_ansi(HEXCodes.DARK_BROWN, Layer.Foreground),
        'DARK_BYZANTIUM': Color.hex_to_ansi(HEXCodes.DARK_BYZANTIUM, Layer.Foreground),
        'DARK_CYAN': Color.hex_to_ansi(HEXCodes.DARK_CYAN, Layer.Foreground),
        'DARK_ELECTRIC_BLUE': Color.hex_to_ansi(HEXCodes.DARK_ELECTRIC_BLUE, Layer.Foreground),
        'DARK_GOLDENROD': Color.hex_to_ansi(HEXCodes.DARK_GOLDENROD, Layer.Foreground),
        'DARK_GREEN_X11': Color.hex_to_ansi(HEXCodes.DARK_GREEN_X11, Layer.Foreground),
        'DARK_JUNGLE_GREEN': Color.hex_to_ansi(HEXCodes.DARK_JUNGLE_GREEN, Layer.Foreground),
        'DARK_KHAKI': Color.hex_to_ansi(HEXCodes.DARK_KHAKI, Layer.Foreground),
        'DARK_LAVA': Color.hex_to_ansi(HEXCodes.DARK_LAVA, Layer.Foreground),
        'DARK_LIVER_HORSES': Color.hex_to_ansi(HEXCodes.DARK_LIVER_HORSES, Layer.Foreground),
        'DARK_MAGENTA': Color.hex_to_ansi(HEXCodes.DARK_MAGENTA, Layer.Foreground),
        'DARK_OLIVE_GREEN': Color.hex_to_ansi(HEXCodes.DARK_OLIVE_GREEN, Layer.Foreground),
        'DARK_ORANGE': Color.hex_to_ansi(HEXCodes.DARK_ORANGE, Layer.Foreground),
        'DARK_ORCHID': Color.hex_to_ansi(HEXCodes.DARK_ORCHID, Layer.Foreground),
        'DARK_PURPLE': Color.hex_to_ansi(HEXCodes.DARK_PURPLE, Layer.Foreground),
        'DARK_RED': Color.hex_to_ansi(HEXCodes.DARK_RED, Layer.Foreground),
        'DARK_SALMON': Color.hex_to_ansi(HEXCodes.DARK_SALMON, Layer.Foreground),
        'DARK_SEA_GREEN': Color.hex_to_ansi(HEXCodes.DARK_SEA_GREEN, Layer.Foreground),
        'DARK_SIENNA': Color.hex_to_ansi(HEXCodes.DARK_SIENNA, Layer.Foreground),
        'DARK_SKY_BLUE': Color.hex_to_ansi(HEXCodes.DARK_SKY_BLUE, Layer.Foreground),
        'DARK_SLATE_BLUE': Color.hex_to_ansi(HEXCodes.DARK_SLATE_BLUE, Layer.Foreground),
        'DARK_SLATE_GRAY': Color.hex_to_ansi(HEXCodes.DARK_SLATE_GRAY, Layer.Foreground),
        'DARK_SPRING_GREEN': Color.hex_to_ansi(HEXCodes.DARK_SPRING_GREEN, Layer.Foreground),
        'DARK_TURQUOISE': Color.hex_to_ansi(HEXCodes.DARK_TURQUOISE, Layer.Foreground),
        'DARK_VIOLET': Color.hex_to_ansi(HEXCodes.DARK_VIOLET, Layer.Foreground),
        'DAVY_S_GREY': Color.hex_to_ansi(HEXCodes.DAVY_S_GREY, Layer.Foreground),
        'DEEP_CERISE': Color.hex_to_ansi(HEXCodes.DEEP_CERISE, Layer.Foreground),
        'DEEP_CHAMPAGNE': Color.hex_to_ansi(HEXCodes.DEEP_CHAMPAGNE, Layer.Foreground),
        'DEEP_CHESTNUT': Color.hex_to_ansi(HEXCodes.DEEP_CHESTNUT, Layer.Foreground),
        'DEEP_JUNGLE_GREEN': Color.hex_to_ansi(HEXCodes.DEEP_JUNGLE_GREEN, Layer.Foreground),
        'DEEP_PINK': Color.hex_to_ansi(HEXCodes.DEEP_PINK, Layer.Foreground),
        'DEEP_SAFFRON': Color.hex_to_ansi(HEXCodes.DEEP_SAFFRON, Layer.Foreground),
        'DEEP_SKY_BLUE': Color.hex_to_ansi(HEXCodes.DEEP_SKY_BLUE, Layer.Foreground),
        'DEEP_SPACE_SPARKLE': Color.hex_to_ansi(HEXCodes.DEEP_SPACE_SPARKLE, Layer.Foreground),
        'DEEP_TAUPE': Color.hex_to_ansi(HEXCodes.DEEP_TAUPE, Layer.Foreground),
        'DENIM': Color.hex_to_ansi(HEXCodes.DENIM, Layer.Foreground),
        'DENIM_BLUE': Color.hex_to_ansi(HEXCodes.DENIM_BLUE, Layer.Foreground),
        'DESERT': Color.hex_to_ansi(HEXCodes.DESERT, Layer.Foreground),
        'DESERT_SAND': Color.hex_to_ansi(HEXCodes.DESERT_SAND, Layer.Foreground),
        'DIM_GRAY': Color.hex_to_ansi(HEXCodes.DIM_GRAY, Layer.Foreground),
        'DODGER_BLUE': Color.hex_to_ansi(HEXCodes.DODGER_BLUE, Layer.Foreground),
        'DRAB_DARK_BROWN': Color.hex_to_ansi(HEXCodes.DRAB_DARK_BROWN, Layer.Foreground),
        'DUKE_BLUE': Color.hex_to_ansi(HEXCodes.DUKE_BLUE, Layer.Foreground),
        'DUTCH_WHITE': Color.hex_to_ansi(HEXCodes.DUTCH_WHITE, Layer.Foreground),
        'EBONY': Color.hex_to_ansi(HEXCodes.EBONY, Layer.Foreground),
        'ECRU': Color.hex_to_ansi(HEXCodes.ECRU, Layer.Foreground),
        'EERIE_BLACK': Color.hex_to_ansi(HEXCodes.EERIE_BLACK, Layer.Foreground),
        'EGGPLANT': Color.hex_to_ansi(HEXCodes.EGGPLANT, Layer.Foreground),
        'EGGSHELL': Color.hex_to_ansi(HEXCodes.EGGSHELL, Layer.Foreground),
        'ELECTRIC_LIME': Color.hex_to_ansi(HEXCodes.ELECTRIC_LIME, Layer.Foreground),
        'ELECTRIC_PURPLE': Color.hex_to_ansi(HEXCodes.ELECTRIC_PURPLE, Layer.Foreground),
        'ELECTRIC_VIOLET': Color.hex_to_ansi(HEXCodes.ELECTRIC_VIOLET, Layer.Foreground),
        'EMERALD': Color.hex_to_ansi(HEXCodes.EMERALD, Layer.Foreground),
        'EMINENCE': Color.hex_to_ansi(HEXCodes.EMINENCE, Layer.Foreground),
        'ENGLISH_LAVENDER': Color.hex_to_ansi(HEXCodes.ENGLISH_LAVENDER, Layer.Foreground),
        'ENGLISH_RED': Color.hex_to_ansi(HEXCodes.ENGLISH_RED, Layer.Foreground),
        'ENGLISH_VERMILLION': Color.hex_to_ansi(HEXCodes.ENGLISH_VERMILLION, Layer.Foreground),
        'ENGLISH_VIOLET': Color.hex_to_ansi(HEXCodes.ENGLISH_VIOLET, Layer.Foreground),
        'ERIN': Color.hex_to_ansi(HEXCodes.ERIN, Layer.Foreground),
        'ETON_BLUE': Color.hex_to_ansi(HEXCodes.ETON_BLUE, Layer.Foreground),
        'FALLOW': Color.hex_to_ansi(HEXCodes.FALLOW, Layer.Foreground),
        'FALU_RED': Color.hex_to_ansi(HEXCodes.FALU_RED, Layer.Foreground),
        'FANDANGO': Color.hex_to_ansi(HEXCodes.FANDANGO, Layer.Foreground),
        'FANDANGO_PINK': Color.hex_to_ansi(HEXCodes.FANDANGO_PINK, Layer.Foreground),
        'FAWN': Color.hex_to_ansi(HEXCodes.FAWN, Layer.Foreground),
        'FERN_GREEN': Color.hex_to_ansi(HEXCodes.FERN_GREEN, Layer.Foreground),
        'FIELD_DRAB': Color.hex_to_ansi(HEXCodes.FIELD_DRAB, Layer.Foreground),
        'FIERY_ROSE': Color.hex_to_ansi(HEXCodes.FIERY_ROSE, Layer.Foreground),
        'FINN': Color.hex_to_ansi(HEXCodes.FINN, Layer.Foreground),
        'FIREBRICK': Color.hex_to_ansi(HEXCodes.FIREBRICK, Layer.Foreground),
        'FIRE_ENGINE_RED': Color.hex_to_ansi(HEXCodes.FIRE_ENGINE_RED, Layer.Foreground),
        'FLAME': Color.hex_to_ansi(HEXCodes.FLAME, Layer.Foreground),
        'FLAX': Color.hex_to_ansi(HEXCodes.FLAX, Layer.Foreground),
        'FLIRT': Color.hex_to_ansi(HEXCodes.FLIRT, Layer.Foreground),
        'FLORAL_WHITE': Color.hex_to_ansi(HEXCodes.FLORAL_WHITE, Layer.Foreground),
        'FOREST_GREEN_WEB': Color.hex_to_ansi(HEXCodes.FOREST_GREEN_WEB, Layer.Foreground),
        'FRENCH_BEIGE': Color.hex_to_ansi(HEXCodes.FRENCH_BEIGE, Layer.Foreground),
        'FRENCH_BISTRE': Color.hex_to_ansi(HEXCodes.FRENCH_BISTRE, Layer.Foreground),
        'FRENCH_BLUE': Color.hex_to_ansi(HEXCodes.FRENCH_BLUE, Layer.Foreground),
        'FRENCH_FUCHSIA': Color.hex_to_ansi(HEXCodes.FRENCH_FUCHSIA, Layer.Foreground),
        'FRENCH_LILAC': Color.hex_to_ansi(HEXCodes.FRENCH_LILAC, Layer.Foreground),
        'FRENCH_LIME': Color.hex_to_ansi(HEXCodes.FRENCH_LIME, Layer.Foreground),
        'FRENCH_MAUVE': Color.hex_to_ansi(HEXCodes.FRENCH_MAUVE, Layer.Foreground),
        'FRENCH_PINK': Color.hex_to_ansi(HEXCodes.FRENCH_PINK, Layer.Foreground),
        'FRENCH_RASPBERRY': Color.hex_to_ansi(HEXCodes.FRENCH_RASPBERRY, Layer.Foreground),
        'FRENCH_SKY_BLUE': Color.hex_to_ansi(HEXCodes.FRENCH_SKY_BLUE, Layer.Foreground),
        'FRENCH_VIOLET': Color.hex_to_ansi(HEXCodes.FRENCH_VIOLET, Layer.Foreground),
        'FROSTBITE': Color.hex_to_ansi(HEXCodes.FROSTBITE, Layer.Foreground),
        'FUCHSIA': Color.hex_to_ansi(HEXCodes.FUCHSIA, Layer.Foreground),
        'FUCHSIA_CRAYOLA': Color.hex_to_ansi(HEXCodes.FUCHSIA_CRAYOLA, Layer.Foreground),
        'FULVOUS': Color.hex_to_ansi(HEXCodes.FULVOUS, Layer.Foreground),
        'FUZZY_WUZZY': Color.hex_to_ansi(HEXCodes.FUZZY_WUZZY, Layer.Foreground),
        'GAINSBORO': Color.hex_to_ansi(HEXCodes.GAINSBORO, Layer.Foreground),
        'GAMBOGE': Color.hex_to_ansi(HEXCodes.GAMBOGE, Layer.Foreground),
        'GENERIC_VIRIDIAN': Color.hex_to_ansi(HEXCodes.GENERIC_VIRIDIAN, Layer.Foreground),
        'GHOST_WHITE': Color.hex_to_ansi(HEXCodes.GHOST_WHITE, Layer.Foreground),
        'GLAUCOUS': Color.hex_to_ansi(HEXCodes.GLAUCOUS, Layer.Foreground),
        'GLOSSY_GRAPE': Color.hex_to_ansi(HEXCodes.GLOSSY_GRAPE, Layer.Foreground),
        'GO_GREEN': Color.hex_to_ansi(HEXCodes.GO_GREEN, Layer.Foreground),
        'GOLD_METALLIC': Color.hex_to_ansi(HEXCodes.GOLD_METALLIC, Layer.Foreground),
        'GOLD_WEB_GOLDEN': Color.hex_to_ansi(HEXCodes.GOLD_WEB_GOLDEN, Layer.Foreground),
        'GOLD_CRAYOLA': Color.hex_to_ansi(HEXCodes.GOLD_CRAYOLA, Layer.Foreground),
        'GOLD_FUSION': Color.hex_to_ansi(HEXCodes.GOLD_FUSION, Layer.Foreground),
        'GOLDEN_BROWN': Color.hex_to_ansi(HEXCodes.GOLDEN_BROWN, Layer.Foreground),
        'GOLDEN_POPPY': Color.hex_to_ansi(HEXCodes.GOLDEN_POPPY, Layer.Foreground),
        'GOLDEN_YELLOW': Color.hex_to_ansi(HEXCodes.GOLDEN_YELLOW, Layer.Foreground),
        'GOLDENROD': Color.hex_to_ansi(HEXCodes.GOLDENROD, Layer.Foreground),
        'GOTHAM_GREEN': Color.hex_to_ansi(HEXCodes.GOTHAM_GREEN, Layer.Foreground),
        'GRANITE_GRAY': Color.hex_to_ansi(HEXCodes.GRANITE_GRAY, Layer.Foreground),
        'GRANNY_SMITH_APPLE': Color.hex_to_ansi(HEXCodes.GRANNY_SMITH_APPLE, Layer.Foreground),
        'GRAY_WEB': Color.hex_to_ansi(HEXCodes.GRAY_WEB, Layer.Foreground),
        'GRAY_X11_GRAY': Color.hex_to_ansi(HEXCodes.GRAY_X11_GRAY, Layer.Foreground),
        'GREEN_CRAYOLA': Color.hex_to_ansi(HEXCodes.GREEN_CRAYOLA, Layer.Foreground),
        'GREEN_WEB': Color.hex_to_ansi(HEXCodes.GREEN_WEB, Layer.Foreground),
        'GREEN_MUNSELL': Color.hex_to_ansi(HEXCodes.GREEN_MUNSELL, Layer.Foreground),
        'GREEN_NCS': Color.hex_to_ansi(HEXCodes.GREEN_NCS, Layer.Foreground),
        'GREEN_PANTONE': Color.hex_to_ansi(HEXCodes.GREEN_PANTONE, Layer.Foreground),
        'GREEN_PIGMENT': Color.hex_to_ansi(HEXCodes.GREEN_PIGMENT, Layer.Foreground),
        'GREEN_BLUE': Color.hex_to_ansi(HEXCodes.GREEN_BLUE, Layer.Foreground),
        'GREEN_LIZARD': Color.hex_to_ansi(HEXCodes.GREEN_LIZARD, Layer.Foreground),
        'GREEN_SHEEN': Color.hex_to_ansi(HEXCodes.GREEN_SHEEN, Layer.Foreground),
        'GUNMETAL': Color.hex_to_ansi(HEXCodes.GUNMETAL, Layer.Foreground),
        'HANSA_YELLOW': Color.hex_to_ansi(HEXCodes.HANSA_YELLOW, Layer.Foreground),
        'HARLEQUIN': Color.hex_to_ansi(HEXCodes.HARLEQUIN, Layer.Foreground),
        'HARVEST_GOLD': Color.hex_to_ansi(HEXCodes.HARVEST_GOLD, Layer.Foreground),
        'HEAT_WAVE': Color.hex_to_ansi(HEXCodes.HEAT_WAVE, Layer.Foreground),
        'HELIOTROPE': Color.hex_to_ansi(HEXCodes.HELIOTROPE, Layer.Foreground),
        'HELIOTROPE_GRAY': Color.hex_to_ansi(HEXCodes.HELIOTROPE_GRAY, Layer.Foreground),
        'HOLLYWOOD_CERISE': Color.hex_to_ansi(HEXCodes.HOLLYWOOD_CERISE, Layer.Foreground),
        'HONOLULU_BLUE': Color.hex_to_ansi(HEXCodes.HONOLULU_BLUE, Layer.Foreground),
        'HOOKER_S_GREEN': Color.hex_to_ansi(HEXCodes.HOOKER_S_GREEN, Layer.Foreground),
        'HOT_MAGENTA': Color.hex_to_ansi(HEXCodes.HOT_MAGENTA, Layer.Foreground),
        'HOT_PINK': Color.hex_to_ansi(HEXCodes.HOT_PINK, Layer.Foreground),
        'HUNTER_GREEN': Color.hex_to_ansi(HEXCodes.HUNTER_GREEN, Layer.Foreground),
        'ICEBERG': Color.hex_to_ansi(HEXCodes.ICEBERG, Layer.Foreground),
        'ILLUMINATING_EMERALD': Color.hex_to_ansi(HEXCodes.ILLUMINATING_EMERALD, Layer.Foreground),
        'IMPERIAL_RED': Color.hex_to_ansi(HEXCodes.IMPERIAL_RED, Layer.Foreground),
        'INCHWORM': Color.hex_to_ansi(HEXCodes.INCHWORM, Layer.Foreground),
        'INDEPENDENCE': Color.hex_to_ansi(HEXCodes.INDEPENDENCE, Layer.Foreground),
        'INDIA_GREEN': Color.hex_to_ansi(HEXCodes.INDIA_GREEN, Layer.Foreground),
        'INDIAN_RED': Color.hex_to_ansi(HEXCodes.INDIAN_RED, Layer.Foreground),
        'INDIAN_YELLOW': Color.hex_to_ansi(HEXCodes.INDIAN_YELLOW, Layer.Foreground),
        'INDIGO': Color.hex_to_ansi(HEXCodes.INDIGO, Layer.Foreground),
        'INDIGO_DYE': Color.hex_to_ansi(HEXCodes.INDIGO_DYE, Layer.Foreground),
        'INTERNATIONAL_KLEIN_BLUE': Color.hex_to_ansi(HEXCodes.INTERNATIONAL_KLEIN_BLUE, Layer.Foreground),
        'INTERNATIONAL_ORANGE_ENGINEERING': Color.hex_to_ansi(
            HEXCodes.INTERNATIONAL_ORANGE_ENGINEERING, Layer.Foreground
        ),
        'INTERNATIONAL_ORANGE_GOLDEN_GATE_BRIDGE': Color.hex_to_ansi(
            HEXCodes.INTERNATIONAL_ORANGE_GOLDEN_GATE_BRIDGE, Layer.Foreground
        ),
        'IRRESISTIBLE': Color.hex_to_ansi(HEXCodes.IRRESISTIBLE, Layer.Foreground),
        'ISABELLINE': Color.hex_to_ansi(HEXCodes.ISABELLINE, Layer.Foreground),
        'ITALIAN_SKY_BLUE': Color.hex_to_ansi(HEXCodes.ITALIAN_SKY_BLUE, Layer.Foreground),
        'IVORY': Color.hex_to_ansi(HEXCodes.IVORY, Layer.Foreground),
        'JAPANESE_CARMINE': Color.hex_to_ansi(HEXCodes.JAPANESE_CARMINE, Layer.Foreground),
        'JAPANESE_VIOLET': Color.hex_to_ansi(HEXCodes.JAPANESE_VIOLET, Layer.Foreground),
        'JASMINE': Color.hex_to_ansi(HEXCodes.JASMINE, Layer.Foreground),
        'JAZZBERRY_JAM': Color.hex_to_ansi(HEXCodes.JAZZBERRY_JAM, Layer.Foreground),
        'JET': Color.hex_to_ansi(HEXCodes.JET, Layer.Foreground),
        'JONQUIL': Color.hex_to_ansi(HEXCodes.JONQUIL, Layer.Foreground),
        'JUNE_BUD': Color.hex_to_ansi(HEXCodes.JUNE_BUD, Layer.Foreground),
        'JUNGLE_GREEN': Color.hex_to_ansi(HEXCodes.JUNGLE_GREEN, Layer.Foreground),
        'KELLY_GREEN': Color.hex_to_ansi(HEXCodes.KELLY_GREEN, Layer.Foreground),
        'KEPPEL': Color.hex_to_ansi(HEXCodes.KEPPEL, Layer.Foreground),
        'KEY_LIME': Color.hex_to_ansi(HEXCodes.KEY_LIME, Layer.Foreground),
        'KHAKI_WEB': Color.hex_to_ansi(HEXCodes.KHAKI_WEB, Layer.Foreground),
        'KHAKI_X11_LIGHT_KHAKI': Color.hex_to_ansi(HEXCodes.KHAKI_X11_LIGHT_KHAKI, Layer.Foreground),
        'KOBE': Color.hex_to_ansi(HEXCodes.KOBE, Layer.Foreground),
        'KOBI': Color.hex_to_ansi(HEXCodes.KOBI, Layer.Foreground),
        'KOBICHA': Color.hex_to_ansi(HEXCodes.KOBICHA, Layer.Foreground),
        'KSU_PURPLE': Color.hex_to_ansi(HEXCodes.KSU_PURPLE, Layer.Foreground),
        'LANGUID_LAVENDER': Color.hex_to_ansi(HEXCodes.LANGUID_LAVENDER, Layer.Foreground),
        'LAPIS_LAZULI': Color.hex_to_ansi(HEXCodes.LAPIS_LAZULI, Layer.Foreground),
        'LASER_LEMON': Color.hex_to_ansi(HEXCodes.LASER_LEMON, Layer.Foreground),
        'LAUREL_GREEN': Color.hex_to_ansi(HEXCodes.LAUREL_GREEN, Layer.Foreground),
        'LAVA': Color.hex_to_ansi(HEXCodes.LAVA, Layer.Foreground),
        'LAVENDER_FLORAL': Color.hex_to_ansi(HEXCodes.LAVENDER_FLORAL, Layer.Foreground),
        'LAVENDER_WEB': Color.hex_to_ansi(HEXCodes.LAVENDER_WEB, Layer.Foreground),
        'LAVENDER_BLUE': Color.hex_to_ansi(HEXCodes.LAVENDER_BLUE, Layer.Foreground),
        'LAVENDER_BLUSH': Color.hex_to_ansi(HEXCodes.LAVENDER_BLUSH, Layer.Foreground),
        'LAVENDER_GRAY': Color.hex_to_ansi(HEXCodes.LAVENDER_GRAY, Layer.Foreground),
        'LAWN_GREEN': Color.hex_to_ansi(HEXCodes.LAWN_GREEN, Layer.Foreground),
        'LEMON': Color.hex_to_ansi(HEXCodes.LEMON, Layer.Foreground),
        'LEMON_CHIFFON': Color.hex_to_ansi(HEXCodes.LEMON_CHIFFON, Layer.Foreground),
        'LEMON_CURRY': Color.hex_to_ansi(HEXCodes.LEMON_CURRY, Layer.Foreground),
        'LEMON_GLACIER': Color.hex_to_ansi(HEXCodes.LEMON_GLACIER, Layer.Foreground),
        'LEMON_MERINGUE': Color.hex_to_ansi(HEXCodes.LEMON_MERINGUE, Layer.Foreground),
        'LEMON_YELLOW': Color.hex_to_ansi(HEXCodes.LEMON_YELLOW, Layer.Foreground),
        'LEMON_YELLOW_CRAYOLA': Color.hex_to_ansi(HEXCodes.LEMON_YELLOW_CRAYOLA, Layer.Foreground),
        'LIBERTY': Color.hex_to_ansi(HEXCodes.LIBERTY, Layer.Foreground),
        'LIGHT_BLUE': Color.hex_to_ansi(HEXCodes.LIGHT_BLUE, Layer.Foreground),
        'LIGHT_CORAL': Color.hex_to_ansi(HEXCodes.LIGHT_CORAL, Layer.Foreground),
        'LIGHT_CORNFLOWER_BLUE': Color.hex_to_ansi(HEXCodes.LIGHT_CORNFLOWER_BLUE, Layer.Foreground),
        'LIGHT_CYAN': Color.hex_to_ansi(HEXCodes.LIGHT_CYAN, Layer.Foreground),
        'LIGHT_FRENCH_BEIGE': Color.hex_to_ansi(HEXCodes.LIGHT_FRENCH_BEIGE, Layer.Foreground),
        'LIGHT_GOLDENROD_YELLOW': Color.hex_to_ansi(HEXCodes.LIGHT_GOLDENROD_YELLOW, Layer.Foreground),
        'LIGHT_GRAY': Color.hex_to_ansi(HEXCodes.LIGHT_GRAY, Layer.Foreground),
        'LIGHT_GREEN': Color.hex_to_ansi(HEXCodes.LIGHT_GREEN, Layer.Foreground),
        'LIGHT_ORANGE': Color.hex_to_ansi(HEXCodes.LIGHT_ORANGE, Layer.Foreground),
        'LIGHT_PERIWINKLE': Color.hex_to_ansi(HEXCodes.LIGHT_PERIWINKLE, Layer.Foreground),
        'LIGHT_PINK': Color.hex_to_ansi(HEXCodes.LIGHT_PINK, Layer.Foreground),
        'LIGHT_SALMON': Color.hex_to_ansi(HEXCodes.LIGHT_SALMON, Layer.Foreground),
        'LIGHT_SEA_GREEN': Color.hex_to_ansi(HEXCodes.LIGHT_SEA_GREEN, Layer.Foreground),
        'LIGHT_SKY_BLUE': Color.hex_to_ansi(HEXCodes.LIGHT_SKY_BLUE, Layer.Foreground),
        'LIGHT_SLATE_GRAY': Color.hex_to_ansi(HEXCodes.LIGHT_SLATE_GRAY, Layer.Foreground),
        'LIGHT_STEEL_BLUE': Color.hex_to_ansi(HEXCodes.LIGHT_STEEL_BLUE, Layer.Foreground),
        'LIGHT_YELLOW': Color.hex_to_ansi(HEXCodes.LIGHT_YELLOW, Layer.Foreground),
        'LILAC': Color.hex_to_ansi(HEXCodes.LILAC, Layer.Foreground),
        'LILAC_LUSTER': Color.hex_to_ansi(HEXCodes.LILAC_LUSTER, Layer.Foreground),
        'LIME_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.LIME_COLOR_WHEEL, Layer.Foreground),
        'LIME_WEB_X11_GREEN': Color.hex_to_ansi(HEXCodes.LIME_WEB_X11_GREEN, Layer.Foreground),
        'LIME_GREEN': Color.hex_to_ansi(HEXCodes.LIME_GREEN, Layer.Foreground),
        'LINCOLN_GREEN': Color.hex_to_ansi(HEXCodes.LINCOLN_GREEN, Layer.Foreground),
        'LINEN': Color.hex_to_ansi(HEXCodes.LINEN, Layer.Foreground),
        'LION': Color.hex_to_ansi(HEXCodes.LION, Layer.Foreground),
        'LISERAN_PURPLE': Color.hex_to_ansi(HEXCodes.LISERAN_PURPLE, Layer.Foreground),
        'LITTLE_BOY_BLUE': Color.hex_to_ansi(HEXCodes.LITTLE_BOY_BLUE, Layer.Foreground),
        'LIVER': Color.hex_to_ansi(HEXCodes.LIVER, Layer.Foreground),
        'LIVER_DOGS': Color.hex_to_ansi(HEXCodes.LIVER_DOGS, Layer.Foreground),
        'LIVER_ORGAN': Color.hex_to_ansi(HEXCodes.LIVER_ORGAN, Layer.Foreground),
        'LIVER_CHESTNUT': Color.hex_to_ansi(HEXCodes.LIVER_CHESTNUT, Layer.Foreground),
        'LIVID': Color.hex_to_ansi(HEXCodes.LIVID, Layer.Foreground),
        'MACARONI_AND_CHEESE': Color.hex_to_ansi(HEXCodes.MACARONI_AND_CHEESE, Layer.Foreground),
        'MADDER_LAKE': Color.hex_to_ansi(HEXCodes.MADDER_LAKE, Layer.Foreground),
        'MAGENTA_CRAYOLA': Color.hex_to_ansi(HEXCodes.MAGENTA_CRAYOLA, Layer.Foreground),
        'MAGENTA_DYE': Color.hex_to_ansi(HEXCodes.MAGENTA_DYE, Layer.Foreground),
        'MAGENTA_PANTONE': Color.hex_to_ansi(HEXCodes.MAGENTA_PANTONE, Layer.Foreground),
        'MAGENTA_PROCESS': Color.hex_to_ansi(HEXCodes.MAGENTA_PROCESS, Layer.Foreground),
        'MAGENTA_HAZE': Color.hex_to_ansi(HEXCodes.MAGENTA_HAZE, Layer.Foreground),
        'MAGIC_MINT': Color.hex_to_ansi(HEXCodes.MAGIC_MINT, Layer.Foreground),
        'MAGNOLIA': Color.hex_to_ansi(HEXCodes.MAGNOLIA, Layer.Foreground),
        'MAHOGANY': Color.hex_to_ansi(HEXCodes.MAHOGANY, Layer.Foreground),
        'MAIZE': Color.hex_to_ansi(HEXCodes.MAIZE, Layer.Foreground),
        'MAIZE_CRAYOLA': Color.hex_to_ansi(HEXCodes.MAIZE_CRAYOLA, Layer.Foreground),
        'MAJORELLE_BLUE': Color.hex_to_ansi(HEXCodes.MAJORELLE_BLUE, Layer.Foreground),
        'MALACHITE': Color.hex_to_ansi(HEXCodes.MALACHITE, Layer.Foreground),
        'MANATEE': Color.hex_to_ansi(HEXCodes.MANATEE, Layer.Foreground),
        'MANDARIN': Color.hex_to_ansi(HEXCodes.MANDARIN, Layer.Foreground),
        'MANGO': Color.hex_to_ansi(HEXCodes.MANGO, Layer.Foreground),
        'MANGO_TANGO': Color.hex_to_ansi(HEXCodes.MANGO_TANGO, Layer.Foreground),
        'MANTIS': Color.hex_to_ansi(HEXCodes.MANTIS, Layer.Foreground),
        'MARDI_GRAS': Color.hex_to_ansi(HEXCodes.MARDI_GRAS, Layer.Foreground),
        'MARIGOLD': Color.hex_to_ansi(HEXCodes.MARIGOLD, Layer.Foreground),
        'MAROON_CRAYOLA': Color.hex_to_ansi(HEXCodes.MAROON_CRAYOLA, Layer.Foreground),
        'MAROON_WEB': Color.hex_to_ansi(HEXCodes.MAROON_WEB, Layer.Foreground),
        'MAROON_X11': Color.hex_to_ansi(HEXCodes.MAROON_X11, Layer.Foreground),
        'MAUVE': Color.hex_to_ansi(HEXCodes.MAUVE, Layer.Foreground),
        'MAUVE_TAUPE': Color.hex_to_ansi(HEXCodes.MAUVE_TAUPE, Layer.Foreground),
        'MAUVELOUS': Color.hex_to_ansi(HEXCodes.MAUVELOUS, Layer.Foreground),
        'MAXIMUM_BLUE': Color.hex_to_ansi(HEXCodes.MAXIMUM_BLUE, Layer.Foreground),
        'MAXIMUM_BLUE_GREEN': Color.hex_to_ansi(HEXCodes.MAXIMUM_BLUE_GREEN, Layer.Foreground),
        'MAXIMUM_BLUE_PURPLE': Color.hex_to_ansi(HEXCodes.MAXIMUM_BLUE_PURPLE, Layer.Foreground),
        'MAXIMUM_GREEN': Color.hex_to_ansi(HEXCodes.MAXIMUM_GREEN, Layer.Foreground),
        'MAXIMUM_GREEN_YELLOW': Color.hex_to_ansi(HEXCodes.MAXIMUM_GREEN_YELLOW, Layer.Foreground),
        'MAXIMUM_PURPLE': Color.hex_to_ansi(HEXCodes.MAXIMUM_PURPLE, Layer.Foreground),
        'MAXIMUM_RED': Color.hex_to_ansi(HEXCodes.MAXIMUM_RED, Layer.Foreground),
        'MAXIMUM_RED_PURPLE': Color.hex_to_ansi(HEXCodes.MAXIMUM_RED_PURPLE, Layer.Foreground),
        'MAXIMUM_YELLOW': Color.hex_to_ansi(HEXCodes.MAXIMUM_YELLOW, Layer.Foreground),
        'MAXIMUM_YELLOW_RED': Color.hex_to_ansi(HEXCodes.MAXIMUM_YELLOW_RED, Layer.Foreground),
        'MAY_GREEN': Color.hex_to_ansi(HEXCodes.MAY_GREEN, Layer.Foreground),
        'MAYA_BLUE': Color.hex_to_ansi(HEXCodes.MAYA_BLUE, Layer.Foreground),
        'MEDIUM_AQUAMARINE': Color.hex_to_ansi(HEXCodes.MEDIUM_AQUAMARINE, Layer.Foreground),
        'MEDIUM_BLUE': Color.hex_to_ansi(HEXCodes.MEDIUM_BLUE, Layer.Foreground),
        'MEDIUM_CANDY_APPLE_RED': Color.hex_to_ansi(HEXCodes.MEDIUM_CANDY_APPLE_RED, Layer.Foreground),
        'MEDIUM_CARMINE': Color.hex_to_ansi(HEXCodes.MEDIUM_CARMINE, Layer.Foreground),
        'MEDIUM_CHAMPAGNE': Color.hex_to_ansi(HEXCodes.MEDIUM_CHAMPAGNE, Layer.Foreground),
        'MEDIUM_ORCHID': Color.hex_to_ansi(HEXCodes.MEDIUM_ORCHID, Layer.Foreground),
        'MEDIUM_PURPLE': Color.hex_to_ansi(HEXCodes.MEDIUM_PURPLE, Layer.Foreground),
        'MEDIUM_SEA_GREEN': Color.hex_to_ansi(HEXCodes.MEDIUM_SEA_GREEN, Layer.Foreground),
        'MEDIUM_SLATE_BLUE': Color.hex_to_ansi(HEXCodes.MEDIUM_SLATE_BLUE, Layer.Foreground),
        'MEDIUM_SPRING_GREEN': Color.hex_to_ansi(HEXCodes.MEDIUM_SPRING_GREEN, Layer.Foreground),
        'MEDIUM_TURQUOISE': Color.hex_to_ansi(HEXCodes.MEDIUM_TURQUOISE, Layer.Foreground),
        'MEDIUM_VIOLET_RED': Color.hex_to_ansi(HEXCodes.MEDIUM_VIOLET_RED, Layer.Foreground),
        'MELLOW_APRICOT': Color.hex_to_ansi(HEXCodes.MELLOW_APRICOT, Layer.Foreground),
        'MELLOW_YELLOW': Color.hex_to_ansi(HEXCodes.MELLOW_YELLOW, Layer.Foreground),
        'MELON': Color.hex_to_ansi(HEXCodes.MELON, Layer.Foreground),
        'METALLIC_GOLD': Color.hex_to_ansi(HEXCodes.METALLIC_GOLD, Layer.Foreground),
        'METALLIC_SEAWEED': Color.hex_to_ansi(HEXCodes.METALLIC_SEAWEED, Layer.Foreground),
        'METALLIC_SUNBURST': Color.hex_to_ansi(HEXCodes.METALLIC_SUNBURST, Layer.Foreground),
        'MEXICAN_PINK': Color.hex_to_ansi(HEXCodes.MEXICAN_PINK, Layer.Foreground),
        'MIDDLE_BLUE': Color.hex_to_ansi(HEXCodes.MIDDLE_BLUE, Layer.Foreground),
        'MIDDLE_BLUE_GREEN': Color.hex_to_ansi(HEXCodes.MIDDLE_BLUE_GREEN, Layer.Foreground),
        'MIDDLE_BLUE_PURPLE': Color.hex_to_ansi(HEXCodes.MIDDLE_BLUE_PURPLE, Layer.Foreground),
        'MIDDLE_GREY': Color.hex_to_ansi(HEXCodes.MIDDLE_GREY, Layer.Foreground),
        'MIDDLE_GREEN': Color.hex_to_ansi(HEXCodes.MIDDLE_GREEN, Layer.Foreground),
        'MIDDLE_GREEN_YELLOW': Color.hex_to_ansi(HEXCodes.MIDDLE_GREEN_YELLOW, Layer.Foreground),
        'MIDDLE_PURPLE': Color.hex_to_ansi(HEXCodes.MIDDLE_PURPLE, Layer.Foreground),
        'MIDDLE_RED': Color.hex_to_ansi(HEXCodes.MIDDLE_RED, Layer.Foreground),
        'MIDDLE_RED_PURPLE': Color.hex_to_ansi(HEXCodes.MIDDLE_RED_PURPLE, Layer.Foreground),
        'MIDDLE_YELLOW': Color.hex_to_ansi(HEXCodes.MIDDLE_YELLOW, Layer.Foreground),
        'MIDDLE_YELLOW_RED': Color.hex_to_ansi(HEXCodes.MIDDLE_YELLOW_RED, Layer.Foreground),
        'MIDNIGHT': Color.hex_to_ansi(HEXCodes.MIDNIGHT, Layer.Foreground),
        'MIDNIGHT_BLUE': Color.hex_to_ansi(HEXCodes.MIDNIGHT_BLUE, Layer.Foreground),
        'MIDNIGHT_GREEN_EAGLE_GREEN': Color.hex_to_ansi(HEXCodes.MIDNIGHT_GREEN_EAGLE_GREEN, Layer.Foreground),
        'MIKADO_YELLOW': Color.hex_to_ansi(HEXCodes.MIKADO_YELLOW, Layer.Foreground),
        'MIMI_PINK': Color.hex_to_ansi(HEXCodes.MIMI_PINK, Layer.Foreground),
        'MINDARO': Color.hex_to_ansi(HEXCodes.MINDARO, Layer.Foreground),
        'MING': Color.hex_to_ansi(HEXCodes.MING, Layer.Foreground),
        'MINION_YELLOW': Color.hex_to_ansi(HEXCodes.MINION_YELLOW, Layer.Foreground),
        'MINT': Color.hex_to_ansi(HEXCodes.MINT, Layer.Foreground),
        'MINT_CREAM': Color.hex_to_ansi(HEXCodes.MINT_CREAM, Layer.Foreground),
        'MINT_GREEN': Color.hex_to_ansi(HEXCodes.MINT_GREEN, Layer.Foreground),
        'MISTY_MOSS': Color.hex_to_ansi(HEXCodes.MISTY_MOSS, Layer.Foreground),
        'MISTY_ROSE': Color.hex_to_ansi(HEXCodes.MISTY_ROSE, Layer.Foreground),
        'MODE_BEIGE': Color.hex_to_ansi(HEXCodes.MODE_BEIGE, Layer.Foreground),
        'MONA_LISA': Color.hex_to_ansi(HEXCodes.MONA_LISA, Layer.Foreground),
        'MORNING_BLUE': Color.hex_to_ansi(HEXCodes.MORNING_BLUE, Layer.Foreground),
        'MOSS_GREEN': Color.hex_to_ansi(HEXCodes.MOSS_GREEN, Layer.Foreground),
        'MOUNTAIN_MEADOW': Color.hex_to_ansi(HEXCodes.MOUNTAIN_MEADOW, Layer.Foreground),
        'MOUNTBATTEN_PINK': Color.hex_to_ansi(HEXCodes.MOUNTBATTEN_PINK, Layer.Foreground),
        'MSU_GREEN': Color.hex_to_ansi(HEXCodes.MSU_GREEN, Layer.Foreground),
        'MULBERRY': Color.hex_to_ansi(HEXCodes.MULBERRY, Layer.Foreground),
        'MULBERRY_CRAYOLA': Color.hex_to_ansi(HEXCodes.MULBERRY_CRAYOLA, Layer.Foreground),
        'MUSTARD': Color.hex_to_ansi(HEXCodes.MUSTARD, Layer.Foreground),
        'MYRTLE_GREEN': Color.hex_to_ansi(HEXCodes.MYRTLE_GREEN, Layer.Foreground),
        'MYSTIC': Color.hex_to_ansi(HEXCodes.MYSTIC, Layer.Foreground),
        'MYSTIC_MAROON': Color.hex_to_ansi(HEXCodes.MYSTIC_MAROON, Layer.Foreground),
        'NADESHIKO_PINK': Color.hex_to_ansi(HEXCodes.NADESHIKO_PINK, Layer.Foreground),
        'NAPLES_YELLOW': Color.hex_to_ansi(HEXCodes.NAPLES_YELLOW, Layer.Foreground),
        'NAVAJO_WHITE': Color.hex_to_ansi(HEXCodes.NAVAJO_WHITE, Layer.Foreground),
        'NAVY_BLUE': Color.hex_to_ansi(HEXCodes.NAVY_BLUE, Layer.Foreground),
        'NAVY_BLUE_CRAYOLA': Color.hex_to_ansi(HEXCodes.NAVY_BLUE_CRAYOLA, Layer.Foreground),
        'NEON_BLUE': Color.hex_to_ansi(HEXCodes.NEON_BLUE, Layer.Foreground),
        'NEON_GREEN': Color.hex_to_ansi(HEXCodes.NEON_GREEN, Layer.Foreground),
        'NEON_FUCHSIA': Color.hex_to_ansi(HEXCodes.NEON_FUCHSIA, Layer.Foreground),
        'NEW_CAR': Color.hex_to_ansi(HEXCodes.NEW_CAR, Layer.Foreground),
        'NEW_YORK_PINK': Color.hex_to_ansi(HEXCodes.NEW_YORK_PINK, Layer.Foreground),
        'NICKEL': Color.hex_to_ansi(HEXCodes.NICKEL, Layer.Foreground),
        'NON_PHOTO_BLUE': Color.hex_to_ansi(HEXCodes.NON_PHOTO_BLUE, Layer.Foreground),
        'NYANZA': Color.hex_to_ansi(HEXCodes.NYANZA, Layer.Foreground),
        'OCHRE': Color.hex_to_ansi(HEXCodes.OCHRE, Layer.Foreground),
        'OLD_BURGUNDY': Color.hex_to_ansi(HEXCodes.OLD_BURGUNDY, Layer.Foreground),
        'OLD_GOLD': Color.hex_to_ansi(HEXCodes.OLD_GOLD, Layer.Foreground),
        'OLD_LACE': Color.hex_to_ansi(HEXCodes.OLD_LACE, Layer.Foreground),
        'OLD_LAVENDER': Color.hex_to_ansi(HEXCodes.OLD_LAVENDER, Layer.Foreground),
        'OLD_MAUVE': Color.hex_to_ansi(HEXCodes.OLD_MAUVE, Layer.Foreground),
        'OLD_ROSE': Color.hex_to_ansi(HEXCodes.OLD_ROSE, Layer.Foreground),
        'OLD_SILVER': Color.hex_to_ansi(HEXCodes.OLD_SILVER, Layer.Foreground),
        'OLIVE': Color.hex_to_ansi(HEXCodes.OLIVE, Layer.Foreground),
        'OLIVE_DRAB_3': Color.hex_to_ansi(HEXCodes.OLIVE_DRAB_3, Layer.Foreground),
        'OLIVE_DRAB_7': Color.hex_to_ansi(HEXCodes.OLIVE_DRAB_7, Layer.Foreground),
        'OLIVE_GREEN': Color.hex_to_ansi(HEXCodes.OLIVE_GREEN, Layer.Foreground),
        'OLIVINE': Color.hex_to_ansi(HEXCodes.OLIVINE, Layer.Foreground),
        'ONYX': Color.hex_to_ansi(HEXCodes.ONYX, Layer.Foreground),
        'OPAL': Color.hex_to_ansi(HEXCodes.OPAL, Layer.Foreground),
        'OPERA_MAUVE': Color.hex_to_ansi(HEXCodes.OPERA_MAUVE, Layer.Foreground),
        'ORANGE': Color.hex_to_ansi(HEXCodes.ORANGE, Layer.Foreground),
        'ORANGE_CRAYOLA': Color.hex_to_ansi(HEXCodes.ORANGE_CRAYOLA, Layer.Foreground),
        'ORANGE_PANTONE': Color.hex_to_ansi(HEXCodes.ORANGE_PANTONE, Layer.Foreground),
        'ORANGE_WEB': Color.hex_to_ansi(HEXCodes.ORANGE_WEB, Layer.Foreground),
        'ORANGE_PEEL': Color.hex_to_ansi(HEXCodes.ORANGE_PEEL, Layer.Foreground),
        'ORANGE_RED': Color.hex_to_ansi(HEXCodes.ORANGE_RED, Layer.Foreground),
        'ORANGE_RED_CRAYOLA': Color.hex_to_ansi(HEXCodes.ORANGE_RED_CRAYOLA, Layer.Foreground),
        'ORANGE_SODA': Color.hex_to_ansi(HEXCodes.ORANGE_SODA, Layer.Foreground),
        'ORANGE_YELLOW': Color.hex_to_ansi(HEXCodes.ORANGE_YELLOW, Layer.Foreground),
        'ORANGE_YELLOW_CRAYOLA': Color.hex_to_ansi(HEXCodes.ORANGE_YELLOW_CRAYOLA, Layer.Foreground),
        'ORCHID': Color.hex_to_ansi(HEXCodes.ORCHID, Layer.Foreground),
        'ORCHID_PINK': Color.hex_to_ansi(HEXCodes.ORCHID_PINK, Layer.Foreground),
        'ORCHID_CRAYOLA': Color.hex_to_ansi(HEXCodes.ORCHID_CRAYOLA, Layer.Foreground),
        'OUTER_SPACE_CRAYOLA': Color.hex_to_ansi(HEXCodes.OUTER_SPACE_CRAYOLA, Layer.Foreground),
        'OUTRAGEOUS_ORANGE': Color.hex_to_ansi(HEXCodes.OUTRAGEOUS_ORANGE, Layer.Foreground),
        'OXBLOOD': Color.hex_to_ansi(HEXCodes.OXBLOOD, Layer.Foreground),
        'OXFORD_BLUE': Color.hex_to_ansi(HEXCodes.OXFORD_BLUE, Layer.Foreground),
        'OU_CRIMSON_RED': Color.hex_to_ansi(HEXCodes.OU_CRIMSON_RED, Layer.Foreground),
        'PACIFIC_BLUE': Color.hex_to_ansi(HEXCodes.PACIFIC_BLUE, Layer.Foreground),
        'PAKISTAN_GREEN': Color.hex_to_ansi(HEXCodes.PAKISTAN_GREEN, Layer.Foreground),
        'PALATINATE_PURPLE': Color.hex_to_ansi(HEXCodes.PALATINATE_PURPLE, Layer.Foreground),
        'PALE_AQUA': Color.hex_to_ansi(HEXCodes.PALE_AQUA, Layer.Foreground),
        'PALE_CERULEAN': Color.hex_to_ansi(HEXCodes.PALE_CERULEAN, Layer.Foreground),
        'PALE_DOGWOOD': Color.hex_to_ansi(HEXCodes.PALE_DOGWOOD, Layer.Foreground),
        'PALE_PINK': Color.hex_to_ansi(HEXCodes.PALE_PINK, Layer.Foreground),
        'PALE_PURPLE_PANTONE': Color.hex_to_ansi(HEXCodes.PALE_PURPLE_PANTONE, Layer.Foreground),
        'PALE_SPRING_BUD': Color.hex_to_ansi(HEXCodes.PALE_SPRING_BUD, Layer.Foreground),
        'PANSY_PURPLE': Color.hex_to_ansi(HEXCodes.PANSY_PURPLE, Layer.Foreground),
        'PAOLO_VERONESE_GREEN': Color.hex_to_ansi(HEXCodes.PAOLO_VERONESE_GREEN, Layer.Foreground),
        'PAPAYA_WHIP': Color.hex_to_ansi(HEXCodes.PAPAYA_WHIP, Layer.Foreground),
        'PARADISE_PINK': Color.hex_to_ansi(HEXCodes.PARADISE_PINK, Layer.Foreground),
        'PARCHMENT': Color.hex_to_ansi(HEXCodes.PARCHMENT, Layer.Foreground),
        'PARIS_GREEN': Color.hex_to_ansi(HEXCodes.PARIS_GREEN, Layer.Foreground),
        'PASTEL_PINK': Color.hex_to_ansi(HEXCodes.PASTEL_PINK, Layer.Foreground),
        'PATRIARCH': Color.hex_to_ansi(HEXCodes.PATRIARCH, Layer.Foreground),
        'PAUA': Color.hex_to_ansi(HEXCodes.PAUA, Layer.Foreground),
        'PAYNE_S_GREY': Color.hex_to_ansi(HEXCodes.PAYNE_S_GREY, Layer.Foreground),
        'PEACH': Color.hex_to_ansi(HEXCodes.PEACH, Layer.Foreground),
        'PEACH_CRAYOLA': Color.hex_to_ansi(HEXCodes.PEACH_CRAYOLA, Layer.Foreground),
        'PEACH_PUFF': Color.hex_to_ansi(HEXCodes.PEACH_PUFF, Layer.Foreground),
        'PEAR': Color.hex_to_ansi(HEXCodes.PEAR, Layer.Foreground),
        'PEARLY_PURPLE': Color.hex_to_ansi(HEXCodes.PEARLY_PURPLE, Layer.Foreground),
        'PERIWINKLE': Color.hex_to_ansi(HEXCodes.PERIWINKLE, Layer.Foreground),
        'PERIWINKLE_CRAYOLA': Color.hex_to_ansi(HEXCodes.PERIWINKLE_CRAYOLA, Layer.Foreground),
        'PERMANENT_GERANIUM_LAKE': Color.hex_to_ansi(HEXCodes.PERMANENT_GERANIUM_LAKE, Layer.Foreground),
        'PERSIAN_BLUE': Color.hex_to_ansi(HEXCodes.PERSIAN_BLUE, Layer.Foreground),
        'PERSIAN_GREEN': Color.hex_to_ansi(HEXCodes.PERSIAN_GREEN, Layer.Foreground),
        'PERSIAN_INDIGO': Color.hex_to_ansi(HEXCodes.PERSIAN_INDIGO, Layer.Foreground),
        'PERSIAN_ORANGE': Color.hex_to_ansi(HEXCodes.PERSIAN_ORANGE, Layer.Foreground),
        'PERSIAN_PINK': Color.hex_to_ansi(HEXCodes.PERSIAN_PINK, Layer.Foreground),
        'PERSIAN_PLUM': Color.hex_to_ansi(HEXCodes.PERSIAN_PLUM, Layer.Foreground),
        'PERSIAN_RED': Color.hex_to_ansi(HEXCodes.PERSIAN_RED, Layer.Foreground),
        'PERSIAN_ROSE': Color.hex_to_ansi(HEXCodes.PERSIAN_ROSE, Layer.Foreground),
        'PERSIMMON': Color.hex_to_ansi(HEXCodes.PERSIMMON, Layer.Foreground),
        'PEWTER_BLUE': Color.hex_to_ansi(HEXCodes.PEWTER_BLUE, Layer.Foreground),
        'PHLOX': Color.hex_to_ansi(HEXCodes.PHLOX, Layer.Foreground),
        'PHTHALO_BLUE': Color.hex_to_ansi(HEXCodes.PHTHALO_BLUE, Layer.Foreground),
        'PHTHALO_GREEN': Color.hex_to_ansi(HEXCodes.PHTHALO_GREEN, Layer.Foreground),
        'PICOTEE_BLUE': Color.hex_to_ansi(HEXCodes.PICOTEE_BLUE, Layer.Foreground),
        'PICTORIAL_CARMINE': Color.hex_to_ansi(HEXCodes.PICTORIAL_CARMINE, Layer.Foreground),
        'PIGGY_PINK': Color.hex_to_ansi(HEXCodes.PIGGY_PINK, Layer.Foreground),
        'PINE_GREEN': Color.hex_to_ansi(HEXCodes.PINE_GREEN, Layer.Foreground),
        'PINK': Color.hex_to_ansi(HEXCodes.PINK, Layer.Foreground),
        'PINK_PANTONE': Color.hex_to_ansi(HEXCodes.PINK_PANTONE, Layer.Foreground),
        'PINK_LACE': Color.hex_to_ansi(HEXCodes.PINK_LACE, Layer.Foreground),
        'PINK_LAVENDER': Color.hex_to_ansi(HEXCodes.PINK_LAVENDER, Layer.Foreground),
        'PINK_SHERBET': Color.hex_to_ansi(HEXCodes.PINK_SHERBET, Layer.Foreground),
        'PISTACHIO': Color.hex_to_ansi(HEXCodes.PISTACHIO, Layer.Foreground),
        'PLATINUM': Color.hex_to_ansi(HEXCodes.PLATINUM, Layer.Foreground),
        'PLUM': Color.hex_to_ansi(HEXCodes.PLUM, Layer.Foreground),
        'PLUM_WEB': Color.hex_to_ansi(HEXCodes.PLUM_WEB, Layer.Foreground),
        'PLUMP_PURPLE': Color.hex_to_ansi(HEXCodes.PLUMP_PURPLE, Layer.Foreground),
        'POLISHED_PINE': Color.hex_to_ansi(HEXCodes.POLISHED_PINE, Layer.Foreground),
        'POMP_AND_POWER': Color.hex_to_ansi(HEXCodes.POMP_AND_POWER, Layer.Foreground),
        'POPSTAR': Color.hex_to_ansi(HEXCodes.POPSTAR, Layer.Foreground),
        'PORTLAND_ORANGE': Color.hex_to_ansi(HEXCodes.PORTLAND_ORANGE, Layer.Foreground),
        'POWDER_BLUE': Color.hex_to_ansi(HEXCodes.POWDER_BLUE, Layer.Foreground),
        'PRAIRIE_GOLD': Color.hex_to_ansi(HEXCodes.PRAIRIE_GOLD, Layer.Foreground),
        'PRINCETON_ORANGE': Color.hex_to_ansi(HEXCodes.PRINCETON_ORANGE, Layer.Foreground),
        'PRUNE': Color.hex_to_ansi(HEXCodes.PRUNE, Layer.Foreground),
        'PRUSSIAN_BLUE': Color.hex_to_ansi(HEXCodes.PRUSSIAN_BLUE, Layer.Foreground),
        'PSYCHEDELIC_PURPLE': Color.hex_to_ansi(HEXCodes.PSYCHEDELIC_PURPLE, Layer.Foreground),
        'PUCE': Color.hex_to_ansi(HEXCodes.PUCE, Layer.Foreground),
        'PULLMAN_BROWN_UPS_BROWN': Color.hex_to_ansi(HEXCodes.PULLMAN_BROWN_UPS_BROWN, Layer.Foreground),
        'PUMPKIN': Color.hex_to_ansi(HEXCodes.PUMPKIN, Layer.Foreground),
        'PURPLE': Color.hex_to_ansi(HEXCodes.PURPLE, Layer.Foreground),
        'PURPLE_WEB': Color.hex_to_ansi(HEXCodes.PURPLE_WEB, Layer.Foreground),
        'PURPLE_MUNSELL': Color.hex_to_ansi(HEXCodes.PURPLE_MUNSELL, Layer.Foreground),
        'PURPLE_X11': Color.hex_to_ansi(HEXCodes.PURPLE_X11, Layer.Foreground),
        'PURPLE_MOUNTAIN_MAJESTY': Color.hex_to_ansi(HEXCodes.PURPLE_MOUNTAIN_MAJESTY, Layer.Foreground),
        'PURPLE_NAVY': Color.hex_to_ansi(HEXCodes.PURPLE_NAVY, Layer.Foreground),
        'PURPLE_PIZZAZZ': Color.hex_to_ansi(HEXCodes.PURPLE_PIZZAZZ, Layer.Foreground),
        'PURPLE_PLUM': Color.hex_to_ansi(HEXCodes.PURPLE_PLUM, Layer.Foreground),
        'PURPUREUS': Color.hex_to_ansi(HEXCodes.PURPUREUS, Layer.Foreground),
        'QUEEN_BLUE': Color.hex_to_ansi(HEXCodes.QUEEN_BLUE, Layer.Foreground),
        'QUEEN_PINK': Color.hex_to_ansi(HEXCodes.QUEEN_PINK, Layer.Foreground),
        'QUICK_SILVER': Color.hex_to_ansi(HEXCodes.QUICK_SILVER, Layer.Foreground),
        'QUINACRIDONE_MAGENTA': Color.hex_to_ansi(HEXCodes.QUINACRIDONE_MAGENTA, Layer.Foreground),
        'RADICAL_RED': Color.hex_to_ansi(HEXCodes.RADICAL_RED, Layer.Foreground),
        'RAISIN_BLACK': Color.hex_to_ansi(HEXCodes.RAISIN_BLACK, Layer.Foreground),
        'RAJAH': Color.hex_to_ansi(HEXCodes.RAJAH, Layer.Foreground),
        'RASPBERRY': Color.hex_to_ansi(HEXCodes.RASPBERRY, Layer.Foreground),
        'RASPBERRY_GLACE': Color.hex_to_ansi(HEXCodes.RASPBERRY_GLACE, Layer.Foreground),
        'RASPBERRY_ROSE': Color.hex_to_ansi(HEXCodes.RASPBERRY_ROSE, Layer.Foreground),
        'RAW_SIENNA': Color.hex_to_ansi(HEXCodes.RAW_SIENNA, Layer.Foreground),
        'RAW_UMBER': Color.hex_to_ansi(HEXCodes.RAW_UMBER, Layer.Foreground),
        'RAZZLE_DAZZLE_ROSE': Color.hex_to_ansi(HEXCodes.RAZZLE_DAZZLE_ROSE, Layer.Foreground),
        'RAZZMATAZZ': Color.hex_to_ansi(HEXCodes.RAZZMATAZZ, Layer.Foreground),
        'RAZZMIC_BERRY': Color.hex_to_ansi(HEXCodes.RAZZMIC_BERRY, Layer.Foreground),
        'REBECCA_PURPLE': Color.hex_to_ansi(HEXCodes.REBECCA_PURPLE, Layer.Foreground),
        'RED_CRAYOLA': Color.hex_to_ansi(HEXCodes.RED_CRAYOLA, Layer.Foreground),
        'RED_MUNSELL': Color.hex_to_ansi(HEXCodes.RED_MUNSELL, Layer.Foreground),
        'RED_NCS': Color.hex_to_ansi(HEXCodes.RED_NCS, Layer.Foreground),
        'RED_PANTONE': Color.hex_to_ansi(HEXCodes.RED_PANTONE, Layer.Foreground),
        'RED_PIGMENT': Color.hex_to_ansi(HEXCodes.RED_PIGMENT, Layer.Foreground),
        'RED_RYB': Color.hex_to_ansi(HEXCodes.RED_RYB, Layer.Foreground),
        'RED_ORANGE': Color.hex_to_ansi(HEXCodes.RED_ORANGE, Layer.Foreground),
        'RED_ORANGE_CRAYOLA': Color.hex_to_ansi(HEXCodes.RED_ORANGE_CRAYOLA, Layer.Foreground),
        'RED_ORANGE_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.RED_ORANGE_COLOR_WHEEL, Layer.Foreground),
        'RED_PURPLE': Color.hex_to_ansi(HEXCodes.RED_PURPLE, Layer.Foreground),
        'RED_SALSA': Color.hex_to_ansi(HEXCodes.RED_SALSA, Layer.Foreground),
        'RED_VIOLET': Color.hex_to_ansi(HEXCodes.RED_VIOLET, Layer.Foreground),
        'RED_VIOLET_CRAYOLA': Color.hex_to_ansi(HEXCodes.RED_VIOLET_CRAYOLA, Layer.Foreground),
        'RED_VIOLET_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.RED_VIOLET_COLOR_WHEEL, Layer.Foreground),
        'REDWOOD': Color.hex_to_ansi(HEXCodes.REDWOOD, Layer.Foreground),
        'RESOLUTION_BLUE': Color.hex_to_ansi(HEXCodes.RESOLUTION_BLUE, Layer.Foreground),
        'RHYTHM': Color.hex_to_ansi(HEXCodes.RHYTHM, Layer.Foreground),
        'RICH_BLACK': Color.hex_to_ansi(HEXCodes.RICH_BLACK, Layer.Foreground),
        'RICH_BLACK_FOGRA29': Color.hex_to_ansi(HEXCodes.RICH_BLACK_FOGRA29, Layer.Foreground),
        'RICH_BLACK_FOGRA39': Color.hex_to_ansi(HEXCodes.RICH_BLACK_FOGRA39, Layer.Foreground),
        'RIFLE_GREEN': Color.hex_to_ansi(HEXCodes.RIFLE_GREEN, Layer.Foreground),
        'ROBIN_EGG_BLUE': Color.hex_to_ansi(HEXCodes.ROBIN_EGG_BLUE, Layer.Foreground),
        'ROCKET_METALLIC': Color.hex_to_ansi(HEXCodes.ROCKET_METALLIC, Layer.Foreground),
        'ROJO_SPANISH_RED': Color.hex_to_ansi(HEXCodes.ROJO_SPANISH_RED, Layer.Foreground),
        'ROMAN_SILVER': Color.hex_to_ansi(HEXCodes.ROMAN_SILVER, Layer.Foreground),
        'ROSE': Color.hex_to_ansi(HEXCodes.ROSE, Layer.Foreground),
        'ROSE_BONBON': Color.hex_to_ansi(HEXCodes.ROSE_BONBON, Layer.Foreground),
        'ROSE_DUST': Color.hex_to_ansi(HEXCodes.ROSE_DUST, Layer.Foreground),
        'ROSE_EBONY': Color.hex_to_ansi(HEXCodes.ROSE_EBONY, Layer.Foreground),
        'ROSE_MADDER': Color.hex_to_ansi(HEXCodes.ROSE_MADDER, Layer.Foreground),
        'ROSE_PINK': Color.hex_to_ansi(HEXCodes.ROSE_PINK, Layer.Foreground),
        'ROSE_POMPADOUR': Color.hex_to_ansi(HEXCodes.ROSE_POMPADOUR, Layer.Foreground),
        'ROSE_RED': Color.hex_to_ansi(HEXCodes.ROSE_RED, Layer.Foreground),
        'ROSE_TAUPE': Color.hex_to_ansi(HEXCodes.ROSE_TAUPE, Layer.Foreground),
        'ROSE_VALE': Color.hex_to_ansi(HEXCodes.ROSE_VALE, Layer.Foreground),
        'ROSEWOOD': Color.hex_to_ansi(HEXCodes.ROSEWOOD, Layer.Foreground),
        'ROSSO_CORSA': Color.hex_to_ansi(HEXCodes.ROSSO_CORSA, Layer.Foreground),
        'ROSY_BROWN': Color.hex_to_ansi(HEXCodes.ROSY_BROWN, Layer.Foreground),
        'ROYAL_BLUE_DARK': Color.hex_to_ansi(HEXCodes.ROYAL_BLUE_DARK, Layer.Foreground),
        'ROYAL_BLUE_LIGHT': Color.hex_to_ansi(HEXCodes.ROYAL_BLUE_LIGHT, Layer.Foreground),
        'ROYAL_PURPLE': Color.hex_to_ansi(HEXCodes.ROYAL_PURPLE, Layer.Foreground),
        'ROYAL_YELLOW': Color.hex_to_ansi(HEXCodes.ROYAL_YELLOW, Layer.Foreground),
        'RUBER': Color.hex_to_ansi(HEXCodes.RUBER, Layer.Foreground),
        'RUBINE_RED': Color.hex_to_ansi(HEXCodes.RUBINE_RED, Layer.Foreground),
        'RUBY': Color.hex_to_ansi(HEXCodes.RUBY, Layer.Foreground),
        'RUBY_RED': Color.hex_to_ansi(HEXCodes.RUBY_RED, Layer.Foreground),
        'RUFOUS': Color.hex_to_ansi(HEXCodes.RUFOUS, Layer.Foreground),
        'RUSSET': Color.hex_to_ansi(HEXCodes.RUSSET, Layer.Foreground),
        'RUSSIAN_GREEN': Color.hex_to_ansi(HEXCodes.RUSSIAN_GREEN, Layer.Foreground),
        'RUSSIAN_VIOLET': Color.hex_to_ansi(HEXCodes.RUSSIAN_VIOLET, Layer.Foreground),
        'RUST': Color.hex_to_ansi(HEXCodes.RUST, Layer.Foreground),
        'RUSTY_RED': Color.hex_to_ansi(HEXCodes.RUSTY_RED, Layer.Foreground),
        'SACRAMENTO_STATE_GREEN': Color.hex_to_ansi(HEXCodes.SACRAMENTO_STATE_GREEN, Layer.Foreground),
        'SADDLE_BROWN': Color.hex_to_ansi(HEXCodes.SADDLE_BROWN, Layer.Foreground),
        'SAFETY_ORANGE': Color.hex_to_ansi(HEXCodes.SAFETY_ORANGE, Layer.Foreground),
        'SAFETY_ORANGE_BLAZE_ORANGE': Color.hex_to_ansi(HEXCodes.SAFETY_ORANGE_BLAZE_ORANGE, Layer.Foreground),
        'SAFETY_YELLOW': Color.hex_to_ansi(HEXCodes.SAFETY_YELLOW, Layer.Foreground),
        'SAFFRON': Color.hex_to_ansi(HEXCodes.SAFFRON, Layer.Foreground),
        'SAGE': Color.hex_to_ansi(HEXCodes.SAGE, Layer.Foreground),
        'ST_PATRICK_S_BLUE': Color.hex_to_ansi(HEXCodes.ST_PATRICK_S_BLUE, Layer.Foreground),
        'SALMON': Color.hex_to_ansi(HEXCodes.SALMON, Layer.Foreground),
        'SALMON_PINK': Color.hex_to_ansi(HEXCodes.SALMON_PINK, Layer.Foreground),
        'SAND': Color.hex_to_ansi(HEXCodes.SAND, Layer.Foreground),
        'SAND_DUNE': Color.hex_to_ansi(HEXCodes.SAND_DUNE, Layer.Foreground),
        'SANDY_BROWN': Color.hex_to_ansi(HEXCodes.SANDY_BROWN, Layer.Foreground),
        'SAP_GREEN': Color.hex_to_ansi(HEXCodes.SAP_GREEN, Layer.Foreground),
        'SAPPHIRE': Color.hex_to_ansi(HEXCodes.SAPPHIRE, Layer.Foreground),
        'SAPPHIRE_BLUE': Color.hex_to_ansi(HEXCodes.SAPPHIRE_BLUE, Layer.Foreground),
        'SAPPHIRE_CRAYOLA': Color.hex_to_ansi(HEXCodes.SAPPHIRE_CRAYOLA, Layer.Foreground),
        'SATIN_SHEEN_GOLD': Color.hex_to_ansi(HEXCodes.SATIN_SHEEN_GOLD, Layer.Foreground),
        'SCARLET': Color.hex_to_ansi(HEXCodes.SCARLET, Layer.Foreground),
        'SCHAUSS_PINK': Color.hex_to_ansi(HEXCodes.SCHAUSS_PINK, Layer.Foreground),
        'SCHOOL_BUS_YELLOW': Color.hex_to_ansi(HEXCodes.SCHOOL_BUS_YELLOW, Layer.Foreground),
        'SCREAMIN_GREEN': Color.hex_to_ansi(HEXCodes.SCREAMIN_GREEN, Layer.Foreground),
        'SEA_GREEN': Color.hex_to_ansi(HEXCodes.SEA_GREEN, Layer.Foreground),
        'SEA_GREEN_CRAYOLA': Color.hex_to_ansi(HEXCodes.SEA_GREEN_CRAYOLA, Layer.Foreground),
        'SEANCE': Color.hex_to_ansi(HEXCodes.SEANCE, Layer.Foreground),
        'SEAL_BROWN': Color.hex_to_ansi(HEXCodes.SEAL_BROWN, Layer.Foreground),
        'SEASHELL': Color.hex_to_ansi(HEXCodes.SEASHELL, Layer.Foreground),
        'SECRET': Color.hex_to_ansi(HEXCodes.SECRET, Layer.Foreground),
        'SELECTIVE_YELLOW': Color.hex_to_ansi(HEXCodes.SELECTIVE_YELLOW, Layer.Foreground),
        'SEPIA': Color.hex_to_ansi(HEXCodes.SEPIA, Layer.Foreground),
        'SHADOW': Color.hex_to_ansi(HEXCodes.SHADOW, Layer.Foreground),
        'SHADOW_BLUE': Color.hex_to_ansi(HEXCodes.SHADOW_BLUE, Layer.Foreground),
        'SHAMROCK_GREEN': Color.hex_to_ansi(HEXCodes.SHAMROCK_GREEN, Layer.Foreground),
        'SHEEN_GREEN': Color.hex_to_ansi(HEXCodes.SHEEN_GREEN, Layer.Foreground),
        'SHIMMERING_BLUSH': Color.hex_to_ansi(HEXCodes.SHIMMERING_BLUSH, Layer.Foreground),
        'SHINY_SHAMROCK': Color.hex_to_ansi(HEXCodes.SHINY_SHAMROCK, Layer.Foreground),
        'SHOCKING_PINK': Color.hex_to_ansi(HEXCodes.SHOCKING_PINK, Layer.Foreground),
        'SHOCKING_PINK_CRAYOLA': Color.hex_to_ansi(HEXCodes.SHOCKING_PINK_CRAYOLA, Layer.Foreground),
        'SIENNA': Color.hex_to_ansi(HEXCodes.SIENNA, Layer.Foreground),
        'SILVER': Color.hex_to_ansi(HEXCodes.SILVER, Layer.Foreground),
        'SILVER_CRAYOLA': Color.hex_to_ansi(HEXCodes.SILVER_CRAYOLA, Layer.Foreground),
        'SILVER_METALLIC': Color.hex_to_ansi(HEXCodes.SILVER_METALLIC, Layer.Foreground),
        'SILVER_CHALICE': Color.hex_to_ansi(HEXCodes.SILVER_CHALICE, Layer.Foreground),
        'SILVER_PINK': Color.hex_to_ansi(HEXCodes.SILVER_PINK, Layer.Foreground),
        'SILVER_SAND': Color.hex_to_ansi(HEXCodes.SILVER_SAND, Layer.Foreground),
        'SINOPIA': Color.hex_to_ansi(HEXCodes.SINOPIA, Layer.Foreground),
        'SIZZLING_RED': Color.hex_to_ansi(HEXCodes.SIZZLING_RED, Layer.Foreground),
        'SIZZLING_SUNRISE': Color.hex_to_ansi(HEXCodes.SIZZLING_SUNRISE, Layer.Foreground),
        'SKOBELOFF': Color.hex_to_ansi(HEXCodes.SKOBELOFF, Layer.Foreground),
        'SKY_BLUE': Color.hex_to_ansi(HEXCodes.SKY_BLUE, Layer.Foreground),
        'SKY_BLUE_CRAYOLA': Color.hex_to_ansi(HEXCodes.SKY_BLUE_CRAYOLA, Layer.Foreground),
        'SKY_MAGENTA': Color.hex_to_ansi(HEXCodes.SKY_MAGENTA, Layer.Foreground),
        'SLATE_BLUE': Color.hex_to_ansi(HEXCodes.SLATE_BLUE, Layer.Foreground),
        'SLATE_GRAY': Color.hex_to_ansi(HEXCodes.SLATE_GRAY, Layer.Foreground),
        'SLIMY_GREEN': Color.hex_to_ansi(HEXCodes.SLIMY_GREEN, Layer.Foreground),
        'SMITTEN': Color.hex_to_ansi(HEXCodes.SMITTEN, Layer.Foreground),
        'SMOKY_BLACK': Color.hex_to_ansi(HEXCodes.SMOKY_BLACK, Layer.Foreground),
        'SNOW': Color.hex_to_ansi(HEXCodes.SNOW, Layer.Foreground),
        'SOLID_PINK': Color.hex_to_ansi(HEXCodes.SOLID_PINK, Layer.Foreground),
        'SONIC_SILVER': Color.hex_to_ansi(HEXCodes.SONIC_SILVER, Layer.Foreground),
        'SPACE_CADET': Color.hex_to_ansi(HEXCodes.SPACE_CADET, Layer.Foreground),
        'SPANISH_BISTRE': Color.hex_to_ansi(HEXCodes.SPANISH_BISTRE, Layer.Foreground),
        'SPANISH_BLUE': Color.hex_to_ansi(HEXCodes.SPANISH_BLUE, Layer.Foreground),
        'SPANISH_CARMINE': Color.hex_to_ansi(HEXCodes.SPANISH_CARMINE, Layer.Foreground),
        'SPANISH_GRAY': Color.hex_to_ansi(HEXCodes.SPANISH_GRAY, Layer.Foreground),
        'SPANISH_GREEN': Color.hex_to_ansi(HEXCodes.SPANISH_GREEN, Layer.Foreground),
        'SPANISH_ORANGE': Color.hex_to_ansi(HEXCodes.SPANISH_ORANGE, Layer.Foreground),
        'SPANISH_PINK': Color.hex_to_ansi(HEXCodes.SPANISH_PINK, Layer.Foreground),
        'SPANISH_RED': Color.hex_to_ansi(HEXCodes.SPANISH_RED, Layer.Foreground),
        'SPANISH_SKY_BLUE': Color.hex_to_ansi(HEXCodes.SPANISH_SKY_BLUE, Layer.Foreground),
        'SPANISH_VIOLET': Color.hex_to_ansi(HEXCodes.SPANISH_VIOLET, Layer.Foreground),
        'SPANISH_VIRIDIAN': Color.hex_to_ansi(HEXCodes.SPANISH_VIRIDIAN, Layer.Foreground),
        'SPRING_BUD': Color.hex_to_ansi(HEXCodes.SPRING_BUD, Layer.Foreground),
        'SPRING_FROST': Color.hex_to_ansi(HEXCodes.SPRING_FROST, Layer.Foreground),
        'SPRING_GREEN': Color.hex_to_ansi(HEXCodes.SPRING_GREEN, Layer.Foreground),
        'SPRING_GREEN_CRAYOLA': Color.hex_to_ansi(HEXCodes.SPRING_GREEN_CRAYOLA, Layer.Foreground),
        'STAR_COMMAND_BLUE': Color.hex_to_ansi(HEXCodes.STAR_COMMAND_BLUE, Layer.Foreground),
        'STEEL_BLUE': Color.hex_to_ansi(HEXCodes.STEEL_BLUE, Layer.Foreground),
        'STEEL_PINK': Color.hex_to_ansi(HEXCodes.STEEL_PINK, Layer.Foreground),
        'STIL_DE_GRAIN_YELLOW': Color.hex_to_ansi(HEXCodes.STIL_DE_GRAIN_YELLOW, Layer.Foreground),
        'STIZZA': Color.hex_to_ansi(HEXCodes.STIZZA, Layer.Foreground),
        'STRAW': Color.hex_to_ansi(HEXCodes.STRAW, Layer.Foreground),
        'STRAWBERRY': Color.hex_to_ansi(HEXCodes.STRAWBERRY, Layer.Foreground),
        'STRAWBERRY_BLONDE': Color.hex_to_ansi(HEXCodes.STRAWBERRY_BLONDE, Layer.Foreground),
        'STRONG_LIME_GREEN': Color.hex_to_ansi(HEXCodes.STRONG_LIME_GREEN, Layer.Foreground),
        'SUGAR_PLUM': Color.hex_to_ansi(HEXCodes.SUGAR_PLUM, Layer.Foreground),
        'SUNGLOW': Color.hex_to_ansi(HEXCodes.SUNGLOW, Layer.Foreground),
        'SUNRAY': Color.hex_to_ansi(HEXCodes.SUNRAY, Layer.Foreground),
        'SUNSET': Color.hex_to_ansi(HEXCodes.SUNSET, Layer.Foreground),
        'SUPER_PINK': Color.hex_to_ansi(HEXCodes.SUPER_PINK, Layer.Foreground),
        'SWEET_BROWN': Color.hex_to_ansi(HEXCodes.SWEET_BROWN, Layer.Foreground),
        'SYRACUSE_ORANGE': Color.hex_to_ansi(HEXCodes.SYRACUSE_ORANGE, Layer.Foreground),
        'TAN': Color.hex_to_ansi(HEXCodes.TAN, Layer.Foreground),
        'TAN_CRAYOLA': Color.hex_to_ansi(HEXCodes.TAN_CRAYOLA, Layer.Foreground),
        'TANGERINE': Color.hex_to_ansi(HEXCodes.TANGERINE, Layer.Foreground),
        'TANGO_PINK': Color.hex_to_ansi(HEXCodes.TANGO_PINK, Layer.Foreground),
        'TART_ORANGE': Color.hex_to_ansi(HEXCodes.TART_ORANGE, Layer.Foreground),
        'TAUPE': Color.hex_to_ansi(HEXCodes.TAUPE, Layer.Foreground),
        'TAUPE_GRAY': Color.hex_to_ansi(HEXCodes.TAUPE_GRAY, Layer.Foreground),
        'TEA_GREEN': Color.hex_to_ansi(HEXCodes.TEA_GREEN, Layer.Foreground),
        'TEA_ROSE': Color.hex_to_ansi(HEXCodes.TEA_ROSE, Layer.Foreground),
        'TEAL': Color.hex_to_ansi(HEXCodes.TEAL, Layer.Foreground),
        'TEAL_BLUE': Color.hex_to_ansi(HEXCodes.TEAL_BLUE, Layer.Foreground),
        'TECHNOBOTANICA': Color.hex_to_ansi(HEXCodes.TECHNOBOTANICA, Layer.Foreground),
        'TELEMAGENTA': Color.hex_to_ansi(HEXCodes.TELEMAGENTA, Layer.Foreground),
        'TENNE_TAWNY': Color.hex_to_ansi(HEXCodes.TENNE_TAWNY, Layer.Foreground),
        'TERRA_COTTA': Color.hex_to_ansi(HEXCodes.TERRA_COTTA, Layer.Foreground),
        'THISTLE': Color.hex_to_ansi(HEXCodes.THISTLE, Layer.Foreground),
        'THULIAN_PINK': Color.hex_to_ansi(HEXCodes.THULIAN_PINK, Layer.Foreground),
        'TICKLE_ME_PINK': Color.hex_to_ansi(HEXCodes.TICKLE_ME_PINK, Layer.Foreground),
        'TIFFANY_BLUE': Color.hex_to_ansi(HEXCodes.TIFFANY_BLUE, Layer.Foreground),
        'TIMBERWOLF': Color.hex_to_ansi(HEXCodes.TIMBERWOLF, Layer.Foreground),
        'TITANIUM_YELLOW': Color.hex_to_ansi(HEXCodes.TITANIUM_YELLOW, Layer.Foreground),
        'TOMATO': Color.hex_to_ansi(HEXCodes.TOMATO, Layer.Foreground),
        'TOURMALINE': Color.hex_to_ansi(HEXCodes.TOURMALINE, Layer.Foreground),
        'TROPICAL_RAINFOREST': Color.hex_to_ansi(HEXCodes.TROPICAL_RAINFOREST, Layer.Foreground),
        'TRUE_BLUE': Color.hex_to_ansi(HEXCodes.TRUE_BLUE, Layer.Foreground),
        'TRYPAN_BLUE': Color.hex_to_ansi(HEXCodes.TRYPAN_BLUE, Layer.Foreground),
        'TUFTS_BLUE': Color.hex_to_ansi(HEXCodes.TUFTS_BLUE, Layer.Foreground),
        'TUMBLEWEED': Color.hex_to_ansi(HEXCodes.TUMBLEWEED, Layer.Foreground),
        'TURQUOISE': Color.hex_to_ansi(HEXCodes.TURQUOISE, Layer.Foreground),
        'TURQUOISE_BLUE': Color.hex_to_ansi(HEXCodes.TURQUOISE_BLUE, Layer.Foreground),
        'TURQUOISE_GREEN': Color.hex_to_ansi(HEXCodes.TURQUOISE_GREEN, Layer.Foreground),
        'TURTLE_GREEN': Color.hex_to_ansi(HEXCodes.TURTLE_GREEN, Layer.Foreground),
        'TUSCAN': Color.hex_to_ansi(HEXCodes.TUSCAN, Layer.Foreground),
        'TUSCAN_BROWN': Color.hex_to_ansi(HEXCodes.TUSCAN_BROWN, Layer.Foreground),
        'TUSCAN_RED': Color.hex_to_ansi(HEXCodes.TUSCAN_RED, Layer.Foreground),
        'TUSCAN_TAN': Color.hex_to_ansi(HEXCodes.TUSCAN_TAN, Layer.Foreground),
        'TUSCANY': Color.hex_to_ansi(HEXCodes.TUSCANY, Layer.Foreground),
        'TWILIGHT_LAVENDER': Color.hex_to_ansi(HEXCodes.TWILIGHT_LAVENDER, Layer.Foreground),
        'TYRIAN_PURPLE': Color.hex_to_ansi(HEXCodes.TYRIAN_PURPLE, Layer.Foreground),
        'UA_BLUE': Color.hex_to_ansi(HEXCodes.UA_BLUE, Layer.Foreground),
        'UA_RED': Color.hex_to_ansi(HEXCodes.UA_RED, Layer.Foreground),
        'ULTRAMARINE': Color.hex_to_ansi(HEXCodes.ULTRAMARINE, Layer.Foreground),
        'ULTRAMARINE_BLUE': Color.hex_to_ansi(HEXCodes.ULTRAMARINE_BLUE, Layer.Foreground),
        'ULTRA_PINK': Color.hex_to_ansi(HEXCodes.ULTRA_PINK, Layer.Foreground),
        'ULTRA_RED': Color.hex_to_ansi(HEXCodes.ULTRA_RED, Layer.Foreground),
        'UMBER': Color.hex_to_ansi(HEXCodes.UMBER, Layer.Foreground),
        'UNBLEACHED_SILK': Color.hex_to_ansi(HEXCodes.UNBLEACHED_SILK, Layer.Foreground),
        'UNITED_NATIONS_BLUE': Color.hex_to_ansi(HEXCodes.UNITED_NATIONS_BLUE, Layer.Foreground),
        'UNIVERSITY_OF_PENNSYLVANIA_RED': Color.hex_to_ansi(HEXCodes.UNIVERSITY_OF_PENNSYLVANIA_RED, Layer.Foreground),
        'UNMELLOW_YELLOW': Color.hex_to_ansi(HEXCodes.UNMELLOW_YELLOW, Layer.Foreground),
        'UP_FOREST_GREEN': Color.hex_to_ansi(HEXCodes.UP_FOREST_GREEN, Layer.Foreground),
        'UP_MAROON': Color.hex_to_ansi(HEXCodes.UP_MAROON, Layer.Foreground),
        'UPSDELL_RED': Color.hex_to_ansi(HEXCodes.UPSDELL_RED, Layer.Foreground),
        'URANIAN_BLUE': Color.hex_to_ansi(HEXCodes.URANIAN_BLUE, Layer.Foreground),
        'USAFA_BLUE': Color.hex_to_ansi(HEXCodes.USAFA_BLUE, Layer.Foreground),
        'VAN_DYKE_BROWN': Color.hex_to_ansi(HEXCodes.VAN_DYKE_BROWN, Layer.Foreground),
        'VANILLA': Color.hex_to_ansi(HEXCodes.VANILLA, Layer.Foreground),
        'VANILLA_ICE': Color.hex_to_ansi(HEXCodes.VANILLA_ICE, Layer.Foreground),
        'VEGAS_GOLD': Color.hex_to_ansi(HEXCodes.VEGAS_GOLD, Layer.Foreground),
        'VENETIAN_RED': Color.hex_to_ansi(HEXCodes.VENETIAN_RED, Layer.Foreground),
        'VERDIGRIS': Color.hex_to_ansi(HEXCodes.VERDIGRIS, Layer.Foreground),
        'VERMILION': Color.hex_to_ansi(HEXCodes.VERMILION, Layer.Foreground),
        'VERONICA': Color.hex_to_ansi(HEXCodes.VERONICA, Layer.Foreground),
        'VIOLET': Color.hex_to_ansi(HEXCodes.VIOLET, Layer.Foreground),
        'VIOLET_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.VIOLET_COLOR_WHEEL, Layer.Foreground),
        'VIOLET_CRAYOLA': Color.hex_to_ansi(HEXCodes.VIOLET_CRAYOLA, Layer.Foreground),
        'VIOLET_RYB': Color.hex_to_ansi(HEXCodes.VIOLET_RYB, Layer.Foreground),
        'VIOLET_WEB': Color.hex_to_ansi(HEXCodes.VIOLET_WEB, Layer.Foreground),
        'VIOLET_BLUE': Color.hex_to_ansi(HEXCodes.VIOLET_BLUE, Layer.Foreground),
        'VIOLET_BLUE_CRAYOLA': Color.hex_to_ansi(HEXCodes.VIOLET_BLUE_CRAYOLA, Layer.Foreground),
        'VIOLET_RED': Color.hex_to_ansi(HEXCodes.VIOLET_RED, Layer.Foreground),
        'VIOLET_REDPERBANG': Color.hex_to_ansi(HEXCodes.VIOLET_REDPERBANG, Layer.Foreground),
        'VIRIDIAN': Color.hex_to_ansi(HEXCodes.VIRIDIAN, Layer.Foreground),
        'VIRIDIAN_GREEN': Color.hex_to_ansi(HEXCodes.VIRIDIAN_GREEN, Layer.Foreground),
        'VIVID_BURGUNDY': Color.hex_to_ansi(HEXCodes.VIVID_BURGUNDY, Layer.Foreground),
        'VIVID_SKY_BLUE': Color.hex_to_ansi(HEXCodes.VIVID_SKY_BLUE, Layer.Foreground),
        'VIVID_TANGERINE': Color.hex_to_ansi(HEXCodes.VIVID_TANGERINE, Layer.Foreground),
        'VIVID_VIOLET': Color.hex_to_ansi(HEXCodes.VIVID_VIOLET, Layer.Foreground),
        'VOLT': Color.hex_to_ansi(HEXCodes.VOLT, Layer.Foreground),
        'WARM_BLACK': Color.hex_to_ansi(HEXCodes.WARM_BLACK, Layer.Foreground),
        'WEEZY_BLUE': Color.hex_to_ansi(HEXCodes.WEEZY_BLUE, Layer.Foreground),
        'WHEAT': Color.hex_to_ansi(HEXCodes.WHEAT, Layer.Foreground),
        'WILD_BLUE_YONDER': Color.hex_to_ansi(HEXCodes.WILD_BLUE_YONDER, Layer.Foreground),
        'WILD_ORCHID': Color.hex_to_ansi(HEXCodes.WILD_ORCHID, Layer.Foreground),
        'WILD_STRAWBERRY': Color.hex_to_ansi(HEXCodes.WILD_STRAWBERRY, Layer.Foreground),
        'WILD_WATERMELON': Color.hex_to_ansi(HEXCodes.WILD_WATERMELON, Layer.Foreground),
        'WINDSOR_TAN': Color.hex_to_ansi(HEXCodes.WINDSOR_TAN, Layer.Foreground),
        'WINE': Color.hex_to_ansi(HEXCodes.WINE, Layer.Foreground),
        'WINE_DREGS': Color.hex_to_ansi(HEXCodes.WINE_DREGS, Layer.Foreground),
        'WINTER_SKY': Color.hex_to_ansi(HEXCodes.WINTER_SKY, Layer.Foreground),
        'WINTERGREEN_DREAM': Color.hex_to_ansi(HEXCodes.WINTERGREEN_DREAM, Layer.Foreground),
        'WISTERIA': Color.hex_to_ansi(HEXCodes.WISTERIA, Layer.Foreground),
        'WOOD_BROWN': Color.hex_to_ansi(HEXCodes.WOOD_BROWN, Layer.Foreground),
        'XANADU': Color.hex_to_ansi(HEXCodes.XANADU, Layer.Foreground),
        'XANTHIC': Color.hex_to_ansi(HEXCodes.XANTHIC, Layer.Foreground),
        'XANTHOUS': Color.hex_to_ansi(HEXCodes.XANTHOUS, Layer.Foreground),
        'YALE_BLUE': Color.hex_to_ansi(HEXCodes.YALE_BLUE, Layer.Foreground),
        'YELLOW_CRAYOLA': Color.hex_to_ansi(HEXCodes.YELLOW_CRAYOLA, Layer.Foreground),
        'YELLOW_MUNSELL': Color.hex_to_ansi(HEXCodes.YELLOW_MUNSELL, Layer.Foreground),
        'YELLOW_NCS': Color.hex_to_ansi(HEXCodes.YELLOW_NCS, Layer.Foreground),
        'YELLOW_PANTONE': Color.hex_to_ansi(HEXCodes.YELLOW_PANTONE, Layer.Foreground),
        'YELLOW_PROCESS': Color.hex_to_ansi(HEXCodes.YELLOW_PROCESS, Layer.Foreground),
        'YELLOW_RYB': Color.hex_to_ansi(HEXCodes.YELLOW_RYB, Layer.Foreground),
        'YELLOW_GREEN': Color.hex_to_ansi(HEXCodes.YELLOW_GREEN, Layer.Foreground),
        'YELLOW_GREEN_CRAYOLA': Color.hex_to_ansi(HEXCodes.YELLOW_GREEN_CRAYOLA, Layer.Foreground),
        'YELLOW_GREEN_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.YELLOW_GREEN_COLOR_WHEEL, Layer.Foreground),
        'YELLOW_ORANGE': Color.hex_to_ansi(HEXCodes.YELLOW_ORANGE, Layer.Foreground),
        'YELLOW_ORANGE_COLOR_WHEEL': Color.hex_to_ansi(HEXCodes.YELLOW_ORANGE_COLOR_WHEEL, Layer.Foreground),
        'YELLOW_SUNSHINE': Color.hex_to_ansi(HEXCodes.YELLOW_SUNSHINE, Layer.Foreground),
        'YINMN_BLUE': Color.hex_to_ansi(HEXCodes.YINMN_BLUE, Layer.Foreground),
        'ZAFFRE': Color.hex_to_ansi(HEXCodes.ZAFFRE, Layer.Foreground),
        'ZINNWALDITE_BROWN': Color.hex_to_ansi(HEXCodes.ZINNWALDITE_BROWN, Layer.Foreground),
        'ZOMP': Color.hex_to_ansi(HEXCodes.ZOMP, Layer.Foreground)
    }

    # Constants defining standard color values
    BLACK: str = _standard_colors['BLACK']
    RED: str = _standard_colors['RED']
    GREEN: str = _standard_colors['GREEN']
    YELLOW: str = _standard_colors['YELLOW']
    BLUE: str = _standard_colors['BLUE']
    MAGENTA: str = _standard_colors['MAGENTA']
    CYAN: str = _standard_colors['CYAN']
    WHITE: str = _standard_colors['WHITE']

    # Constants defining true color values
    ABSOLUTE_ZERO: str = _true_colors['ABSOLUTE_ZERO']
    ACID_GREEN: str = _true_colors['ACID_GREEN']
    AERO: str = _true_colors['AERO']
    AFRICAN_VIOLET: str = _true_colors['AFRICAN_VIOLET']
    AIR_SUPERIORITY_BLUE: str = _true_colors['AIR_SUPERIORITY_BLUE']
    ALICE_BLUE: str = _true_colors['ALICE_BLUE']
    ALIZARIN: str = _true_colors['ALIZARIN']
    ALLOY_ORANGE: str = _true_colors['ALLOY_ORANGE']
    ALMOND: str = _true_colors['ALMOND']
    AMARANTH_DEEP_PURPLE: str = _true_colors['AMARANTH_DEEP_PURPLE']
    AMARANTH_PINK: str = _true_colors['AMARANTH_PINK']
    AMARANTH_PURPLE: str = _true_colors['AMARANTH_PURPLE']
    AMAZON: str = _true_colors['AMAZON']
    AMBER: str = _true_colors['AMBER']
    AMETHYST: str = _true_colors['AMETHYST']
    ANDROID_GREEN: str = _true_colors['ANDROID_GREEN']
    ANTIQUE_BRASS: str = _true_colors['ANTIQUE_BRASS']
    ANTIQUE_BRONZE: str = _true_colors['ANTIQUE_BRONZE']
    ANTIQUE_FUCHSIA: str = _true_colors['ANTIQUE_FUCHSIA']
    ANTIQUE_RUBY: str = _true_colors['ANTIQUE_RUBY']
    ANTIQUE_WHITE: str = _true_colors['ANTIQUE_WHITE']
    APRICOT: str = _true_colors['APRICOT']
    AQUA: str = _true_colors['AQUA']
    AQUAMARINE: str = _true_colors['AQUAMARINE']
    ARCTIC_LIME: str = _true_colors['ARCTIC_LIME']
    ARTICHOKE_GREEN: str = _true_colors['ARTICHOKE_GREEN']
    ARYLIDE_YELLOW: str = _true_colors['ARYLIDE_YELLOW']
    ASH_GRAY: str = _true_colors['ASH_GRAY']
    ATOMIC_TANGERINE: str = _true_colors['ATOMIC_TANGERINE']
    AUREOLIN: str = _true_colors['AUREOLIN']
    AZURE: str = _true_colors['AZURE']
    BABY_BLUE: str = _true_colors['BABY_BLUE']
    BABY_BLUE_EYES: str = _true_colors['BABY_BLUE_EYES']
    BABY_PINK: str = _true_colors['BABY_PINK']
    BABY_POWDER: str = _true_colors['BABY_POWDER']
    BAKER_MILLER_PINK: str = _true_colors['BAKER_MILLER_PINK']
    BANANA_MANIA: str = _true_colors['BANANA_MANIA']
    BARBIE_PINK: str = _true_colors['BARBIE_PINK']
    BARN_RED: str = _true_colors['BARN_RED']
    BATTLESHIP_GREY: str = _true_colors['BATTLESHIP_GREY']
    BEAU_BLUE: str = _true_colors['BEAU_BLUE']
    BEAVER: str = _true_colors['BEAVER']
    BEIGE: str = _true_colors['BEIGE']
    B_DAZZLED_BLUE: str = _true_colors['B_DAZZLED_BLUE']
    BIG_DIP_O_RUBY: str = _true_colors['BIG_DIP_O_RUBY']
    BISQUE: str = _true_colors['BISQUE']
    BISTRE: str = _true_colors['BISTRE']
    BISTRE_BROWN: str = _true_colors['BISTRE_BROWN']
    BITTER_LEMON: str = _true_colors['BITTER_LEMON']
    BLACK_BEAN: str = _true_colors['BLACK_BEAN']
    BLACK_CORAL: str = _true_colors['BLACK_CORAL']
    BLACK_OLIVE: str = _true_colors['BLACK_OLIVE']
    BLACK_SHADOWS: str = _true_colors['BLACK_SHADOWS']
    BLANCHED_ALMOND: str = _true_colors['BLANCHED_ALMOND']
    BLAST_OFF_BRONZE: str = _true_colors['BLAST_OFF_BRONZE']
    BLEU_DE_FRANCE: str = _true_colors['BLEU_DE_FRANCE']
    BLIZZARD_BLUE: str = _true_colors['BLIZZARD_BLUE']
    BLOOD_RED: str = _true_colors['BLOOD_RED']
    BLUE_CRAYOLA: str = _true_colors['BLUE_CRAYOLA']
    BLUE_MUNSELL: str = _true_colors['BLUE_MUNSELL']
    BLUE_NCS: str = _true_colors['BLUE_NCS']
    BLUE_PANTONE: str = _true_colors['BLUE_PANTONE']
    BLUE_PIGMENT: str = _true_colors['BLUE_PIGMENT']
    BLUE_BELL: str = _true_colors['BLUE_BELL']
    BLUE_GRAY_CRAYOLA: str = _true_colors['BLUE_GRAY_CRAYOLA']
    BLUE_JEANS: str = _true_colors['BLUE_JEANS']
    BLUE_SAPPHIRE: str = _true_colors['BLUE_SAPPHIRE']
    BLUE_VIOLET: str = _true_colors['BLUE_VIOLET']
    BLUE_YONDER: str = _true_colors['BLUE_YONDER']
    BLUETIFUL: str = _true_colors['BLUETIFUL']
    BLUSH: str = _true_colors['BLUSH']
    BOLE: str = _true_colors['BOLE']
    BONE: str = _true_colors['BONE']
    BRICK_RED: str = _true_colors['BRICK_RED']
    BRIGHT_LILAC: str = _true_colors['BRIGHT_LILAC']
    BRIGHT_YELLOW_CRAYOLA: str = _true_colors['BRIGHT_YELLOW_CRAYOLA']
    BRITISH_RACING_GREEN: str = _true_colors['BRITISH_RACING_GREEN']
    BRONZE: str = _true_colors['BRONZE']
    BROWN: str = _true_colors['BROWN']
    BROWN_SUGAR: str = _true_colors['BROWN_SUGAR']
    BUD_GREEN: str = _true_colors['BUD_GREEN']
    BUFF: str = _true_colors['BUFF']
    BURGUNDY: str = _true_colors['BURGUNDY']
    BURLYWOOD: str = _true_colors['BURLYWOOD']
    BURNISHED_BROWN: str = _true_colors['BURNISHED_BROWN']
    BURNT_ORANGE: str = _true_colors['BURNT_ORANGE']
    BURNT_SIENNA: str = _true_colors['BURNT_SIENNA']
    BURNT_UMBER: str = _true_colors['BURNT_UMBER']
    BYZANTINE: str = _true_colors['BYZANTINE']
    BYZANTIUM: str = _true_colors['BYZANTIUM']
    CADET_BLUE: str = _true_colors['CADET_BLUE']
    CADET_GREY: str = _true_colors['CADET_GREY']
    CADMIUM_GREEN: str = _true_colors['CADMIUM_GREEN']
    CADMIUM_ORANGE: str = _true_colors['CADMIUM_ORANGE']
    CAFE_AU_LAIT: str = _true_colors['CAFE_AU_LAIT']
    CAFE_NOIR: str = _true_colors['CAFE_NOIR']
    CAMBRIDGE_BLUE: str = _true_colors['CAMBRIDGE_BLUE']
    CAMEL: str = _true_colors['CAMEL']
    CAMEO_PINK: str = _true_colors['CAMEO_PINK']
    CANARY: str = _true_colors['CANARY']
    CANARY_YELLOW: str = _true_colors['CANARY_YELLOW']
    CANDY_PINK: str = _true_colors['CANDY_PINK']
    CARDINAL: str = _true_colors['CARDINAL']
    CARIBBEAN_GREEN: str = _true_colors['CARIBBEAN_GREEN']
    CARMINE: str = _true_colors['CARMINE']
    CARMINE_M_P: str = _true_colors['CARMINE_M_P']
    CARNATION_PINK: str = _true_colors['CARNATION_PINK']
    CARNELIAN: str = _true_colors['CARNELIAN']
    CAROLINA_BLUE: str = _true_colors['CAROLINA_BLUE']
    CARROT_ORANGE: str = _true_colors['CARROT_ORANGE']
    CATAWBA: str = _true_colors['CATAWBA']
    CEDAR_CHEST: str = _true_colors['CEDAR_CHEST']
    CELADON: str = _true_colors['CELADON']
    CELESTE: str = _true_colors['CELESTE']
    CERISE: str = _true_colors['CERISE']
    CERULEAN: str = _true_colors['CERULEAN']
    CERULEAN_BLUE: str = _true_colors['CERULEAN_BLUE']
    CERULEAN_FROST: str = _true_colors['CERULEAN_FROST']
    CERULEAN_CRAYOLA: str = _true_colors['CERULEAN_CRAYOLA']
    CERULEAN_RGB: str = _true_colors['CERULEAN_RGB']
    CHAMPAGNE: str = _true_colors['CHAMPAGNE']
    CHAMPAGNE_PINK: str = _true_colors['CHAMPAGNE_PINK']
    CHARCOAL: str = _true_colors['CHARCOAL']
    CHARM_PINK: str = _true_colors['CHARM_PINK']
    CHARTREUSE_WEB: str = _true_colors['CHARTREUSE_WEB']
    CHERRY_BLOSSOM_PINK: str = _true_colors['CHERRY_BLOSSOM_PINK']
    CHESTNUT: str = _true_colors['CHESTNUT']
    CHILI_RED: str = _true_colors['CHILI_RED']
    CHINA_PINK: str = _true_colors['CHINA_PINK']
    CHINESE_RED: str = _true_colors['CHINESE_RED']
    CHINESE_VIOLET: str = _true_colors['CHINESE_VIOLET']
    CHINESE_YELLOW: str = _true_colors['CHINESE_YELLOW']
    CHOCOLATE_TRADITIONAL: str = _true_colors['CHOCOLATE_TRADITIONAL']
    CHOCOLATE_WEB: str = _true_colors['CHOCOLATE_WEB']
    CINEREOUS: str = _true_colors['CINEREOUS']
    CINNABAR: str = _true_colors['CINNABAR']
    CINNAMON_SATIN: str = _true_colors['CINNAMON_SATIN']
    CITRINE: str = _true_colors['CITRINE']
    CITRON: str = _true_colors['CITRON']
    CLARET: str = _true_colors['CLARET']
    COFFEE: str = _true_colors['COFFEE']
    COLUMBIA_BLUE: str = _true_colors['COLUMBIA_BLUE']
    CONGO_PINK: str = _true_colors['CONGO_PINK']
    COOL_GREY: str = _true_colors['COOL_GREY']
    COPPER: str = _true_colors['COPPER']
    COPPER_CRAYOLA: str = _true_colors['COPPER_CRAYOLA']
    COPPER_PENNY: str = _true_colors['COPPER_PENNY']
    COPPER_RED: str = _true_colors['COPPER_RED']
    COPPER_ROSE: str = _true_colors['COPPER_ROSE']
    COQUELICOT: str = _true_colors['COQUELICOT']
    CORAL: str = _true_colors['CORAL']
    CORAL_PINK: str = _true_colors['CORAL_PINK']
    CORDOVAN: str = _true_colors['CORDOVAN']
    CORN: str = _true_colors['CORN']
    CORNFLOWER_BLUE: str = _true_colors['CORNFLOWER_BLUE']
    CORNSILK: str = _true_colors['CORNSILK']
    COSMIC_COBALT: str = _true_colors['COSMIC_COBALT']
    COSMIC_LATTE: str = _true_colors['COSMIC_LATTE']
    COYOTE_BROWN: str = _true_colors['COYOTE_BROWN']
    COTTON_CANDY: str = _true_colors['COTTON_CANDY']
    CREAM: str = _true_colors['CREAM']
    CRIMSON: str = _true_colors['CRIMSON']
    CRIMSON_UA: str = _true_colors['CRIMSON_UA']
    CULTURED_PEARL: str = _true_colors['CULTURED_PEARL']
    CYAN_PROCESS: str = _true_colors['CYAN_PROCESS']
    CYBER_GRAPE: str = _true_colors['CYBER_GRAPE']
    CYBER_YELLOW: str = _true_colors['CYBER_YELLOW']
    CYCLAMEN: str = _true_colors['CYCLAMEN']
    DANDELION: str = _true_colors['DANDELION']
    DARK_BROWN: str = _true_colors['DARK_BROWN']
    DARK_BYZANTIUM: str = _true_colors['DARK_BYZANTIUM']
    DARK_CYAN: str = _true_colors['DARK_CYAN']
    DARK_ELECTRIC_BLUE: str = _true_colors['DARK_ELECTRIC_BLUE']
    DARK_GOLDENROD: str = _true_colors['DARK_GOLDENROD']
    DARK_GREEN_X11: str = _true_colors['DARK_GREEN_X11']
    DARK_JUNGLE_GREEN: str = _true_colors['DARK_JUNGLE_GREEN']
    DARK_KHAKI: str = _true_colors['DARK_KHAKI']
    DARK_LAVA: str = _true_colors['DARK_LAVA']
    DARK_LIVER_HORSES: str = _true_colors['DARK_LIVER_HORSES']
    DARK_MAGENTA: str = _true_colors['DARK_MAGENTA']
    DARK_OLIVE_GREEN: str = _true_colors['DARK_OLIVE_GREEN']
    DARK_ORANGE: str = _true_colors['DARK_ORANGE']
    DARK_ORCHID: str = _true_colors['DARK_ORCHID']
    DARK_PURPLE: str = _true_colors['DARK_PURPLE']
    DARK_RED: str = _true_colors['DARK_RED']
    DARK_SALMON: str = _true_colors['DARK_SALMON']
    DARK_SEA_GREEN: str = _true_colors['DARK_SEA_GREEN']
    DARK_SIENNA: str = _true_colors['DARK_SIENNA']
    DARK_SKY_BLUE: str = _true_colors['DARK_SKY_BLUE']
    DARK_SLATE_BLUE: str = _true_colors['DARK_SLATE_BLUE']
    DARK_SLATE_GRAY: str = _true_colors['DARK_SLATE_GRAY']
    DARK_SPRING_GREEN: str = _true_colors['DARK_SPRING_GREEN']
    DARK_TURQUOISE: str = _true_colors['DARK_TURQUOISE']
    DARK_VIOLET: str = _true_colors['DARK_VIOLET']
    DAVY_S_GREY: str = _true_colors['DAVY_S_GREY']
    DEEP_CERISE: str = _true_colors['DEEP_CERISE']
    DEEP_CHAMPAGNE: str = _true_colors['DEEP_CHAMPAGNE']
    DEEP_CHESTNUT: str = _true_colors['DEEP_CHESTNUT']
    DEEP_JUNGLE_GREEN: str = _true_colors['DEEP_JUNGLE_GREEN']
    DEEP_PINK: str = _true_colors['DEEP_PINK']
    DEEP_SAFFRON: str = _true_colors['DEEP_SAFFRON']
    DEEP_SKY_BLUE: str = _true_colors['DEEP_SKY_BLUE']
    DEEP_SPACE_SPARKLE: str = _true_colors['DEEP_SPACE_SPARKLE']
    DEEP_TAUPE: str = _true_colors['DEEP_TAUPE']
    DENIM: str = _true_colors['DENIM']
    DENIM_BLUE: str = _true_colors['DENIM_BLUE']
    DESERT: str = _true_colors['DESERT']
    DESERT_SAND: str = _true_colors['DESERT_SAND']
    DIM_GRAY: str = _true_colors['DIM_GRAY']
    DODGER_BLUE: str = _true_colors['DODGER_BLUE']
    DRAB_DARK_BROWN: str = _true_colors['DRAB_DARK_BROWN']
    DUKE_BLUE: str = _true_colors['DUKE_BLUE']
    DUTCH_WHITE: str = _true_colors['DUTCH_WHITE']
    EBONY: str = _true_colors['EBONY']
    ECRU: str = _true_colors['ECRU']
    EERIE_BLACK: str = _true_colors['EERIE_BLACK']
    EGGPLANT: str = _true_colors['EGGPLANT']
    EGGSHELL: str = _true_colors['EGGSHELL']
    ELECTRIC_LIME: str = _true_colors['ELECTRIC_LIME']
    ELECTRIC_PURPLE: str = _true_colors['ELECTRIC_PURPLE']
    ELECTRIC_VIOLET: str = _true_colors['ELECTRIC_VIOLET']
    EMERALD: str = _true_colors['EMERALD']
    EMINENCE: str = _true_colors['EMINENCE']
    ENGLISH_LAVENDER: str = _true_colors['ENGLISH_LAVENDER']
    ENGLISH_RED: str = _true_colors['ENGLISH_RED']
    ENGLISH_VERMILLION: str = _true_colors['ENGLISH_VERMILLION']
    ENGLISH_VIOLET: str = _true_colors['ENGLISH_VIOLET']
    ERIN: str = _true_colors['ERIN']
    ETON_BLUE: str = _true_colors['ETON_BLUE']
    FALLOW: str = _true_colors['FALLOW']
    FALU_RED: str = _true_colors['FALU_RED']
    FANDANGO: str = _true_colors['FANDANGO']
    FANDANGO_PINK: str = _true_colors['FANDANGO_PINK']
    FAWN: str = _true_colors['FAWN']
    FERN_GREEN: str = _true_colors['FERN_GREEN']
    FIELD_DRAB: str = _true_colors['FIELD_DRAB']
    FIERY_ROSE: str = _true_colors['FIERY_ROSE']
    FINN: str = _true_colors['FINN']
    FIREBRICK: str = _true_colors['FIREBRICK']
    FIRE_ENGINE_RED: str = _true_colors['FIRE_ENGINE_RED']
    FLAME: str = _true_colors['FLAME']
    FLAX: str = _true_colors['FLAX']
    FLIRT: str = _true_colors['FLIRT']
    FLORAL_WHITE: str = _true_colors['FLORAL_WHITE']
    FOREST_GREEN_WEB: str = _true_colors['FOREST_GREEN_WEB']
    FRENCH_BEIGE: str = _true_colors['FRENCH_BEIGE']
    FRENCH_BISTRE: str = _true_colors['FRENCH_BISTRE']
    FRENCH_BLUE: str = _true_colors['FRENCH_BLUE']
    FRENCH_FUCHSIA: str = _true_colors['FRENCH_FUCHSIA']
    FRENCH_LILAC: str = _true_colors['FRENCH_LILAC']
    FRENCH_LIME: str = _true_colors['FRENCH_LIME']
    FRENCH_MAUVE: str = _true_colors['FRENCH_MAUVE']
    FRENCH_PINK: str = _true_colors['FRENCH_PINK']
    FRENCH_RASPBERRY: str = _true_colors['FRENCH_RASPBERRY']
    FRENCH_SKY_BLUE: str = _true_colors['FRENCH_SKY_BLUE']
    FRENCH_VIOLET: str = _true_colors['FRENCH_VIOLET']
    FROSTBITE: str = _true_colors['FROSTBITE']
    FUCHSIA: str = _true_colors['FUCHSIA']
    FUCHSIA_CRAYOLA: str = _true_colors['FUCHSIA_CRAYOLA']
    FULVOUS: str = _true_colors['FULVOUS']
    FUZZY_WUZZY: str = _true_colors['FUZZY_WUZZY']
    GAINSBORO: str = _true_colors['GAINSBORO']
    GAMBOGE: str = _true_colors['GAMBOGE']
    GENERIC_VIRIDIAN: str = _true_colors['GENERIC_VIRIDIAN']
    GHOST_WHITE: str = _true_colors['GHOST_WHITE']
    GLAUCOUS: str = _true_colors['GLAUCOUS']
    GLOSSY_GRAPE: str = _true_colors['GLOSSY_GRAPE']
    GO_GREEN: str = _true_colors['GO_GREEN']
    GOLD_METALLIC: str = _true_colors['GOLD_METALLIC']
    GOLD_WEB_GOLDEN: str = _true_colors['GOLD_WEB_GOLDEN']
    GOLD_CRAYOLA: str = _true_colors['GOLD_CRAYOLA']
    GOLD_FUSION: str = _true_colors['GOLD_FUSION']
    GOLDEN_BROWN: str = _true_colors['GOLDEN_BROWN']
    GOLDEN_POPPY: str = _true_colors['GOLDEN_POPPY']
    GOLDEN_YELLOW: str = _true_colors['GOLDEN_YELLOW']
    GOLDENROD: str = _true_colors['GOLDENROD']
    GOTHAM_GREEN: str = _true_colors['GOTHAM_GREEN']
    GRANITE_GRAY: str = _true_colors['GRANITE_GRAY']
    GRANNY_SMITH_APPLE: str = _true_colors['GRANNY_SMITH_APPLE']
    GRAY_WEB: str = _true_colors['GRAY_WEB']
    GRAY_X11_GRAY: str = _true_colors['GRAY_X11_GRAY']
    GREEN_CRAYOLA: str = _true_colors['GREEN_CRAYOLA']
    GREEN_WEB: str = _true_colors['GREEN_WEB']
    GREEN_MUNSELL: str = _true_colors['GREEN_MUNSELL']
    GREEN_NCS: str = _true_colors['GREEN_NCS']
    GREEN_PANTONE: str = _true_colors['GREEN_PANTONE']
    GREEN_PIGMENT: str = _true_colors['GREEN_PIGMENT']
    GREEN_BLUE: str = _true_colors['GREEN_BLUE']
    GREEN_LIZARD: str = _true_colors['GREEN_LIZARD']
    GREEN_SHEEN: str = _true_colors['GREEN_SHEEN']
    GUNMETAL: str = _true_colors['GUNMETAL']
    HANSA_YELLOW: str = _true_colors['HANSA_YELLOW']
    HARLEQUIN: str = _true_colors['HARLEQUIN']
    HARVEST_GOLD: str = _true_colors['HARVEST_GOLD']
    HEAT_WAVE: str = _true_colors['HEAT_WAVE']
    HELIOTROPE: str = _true_colors['HELIOTROPE']
    HELIOTROPE_GRAY: str = _true_colors['HELIOTROPE_GRAY']
    HOLLYWOOD_CERISE: str = _true_colors['HOLLYWOOD_CERISE']
    HONOLULU_BLUE: str = _true_colors['HONOLULU_BLUE']
    HOOKER_S_GREEN: str = _true_colors['HOOKER_S_GREEN']
    HOT_MAGENTA: str = _true_colors['HOT_MAGENTA']
    HOT_PINK: str = _true_colors['HOT_PINK']
    HUNTER_GREEN: str = _true_colors['HUNTER_GREEN']
    ICEBERG: str = _true_colors['ICEBERG']
    ILLUMINATING_EMERALD: str = _true_colors['ILLUMINATING_EMERALD']
    IMPERIAL_RED: str = _true_colors['IMPERIAL_RED']
    INCHWORM: str = _true_colors['INCHWORM']
    INDEPENDENCE: str = _true_colors['INDEPENDENCE']
    INDIA_GREEN: str = _true_colors['INDIA_GREEN']
    INDIAN_RED: str = _true_colors['INDIAN_RED']
    INDIAN_YELLOW: str = _true_colors['INDIAN_YELLOW']
    INDIGO: str = _true_colors['INDIGO']
    INDIGO_DYE: str = _true_colors['INDIGO_DYE']
    INTERNATIONAL_KLEIN_BLUE: str = _true_colors['INTERNATIONAL_KLEIN_BLUE']
    INTERNATIONAL_ORANGE_ENGINEERING: str = _true_colors['INTERNATIONAL_ORANGE_ENGINEERING']
    INTERNATIONAL_ORANGE_GOLDEN_GATE_BRIDGE: str = _true_colors['INTERNATIONAL_ORANGE_GOLDEN_GATE_BRIDGE']
    IRRESISTIBLE: str = _true_colors['IRRESISTIBLE']
    ISABELLINE: str = _true_colors['ISABELLINE']
    ITALIAN_SKY_BLUE: str = _true_colors['ITALIAN_SKY_BLUE']
    IVORY: str = _true_colors['IVORY']
    JAPANESE_CARMINE: str = _true_colors['JAPANESE_CARMINE']
    JAPANESE_VIOLET: str = _true_colors['JAPANESE_VIOLET']
    JASMINE: str = _true_colors['JASMINE']
    JAZZBERRY_JAM: str = _true_colors['JAZZBERRY_JAM']
    JET: str = _true_colors['JET']
    JONQUIL: str = _true_colors['JONQUIL']
    JUNE_BUD: str = _true_colors['JUNE_BUD']
    JUNGLE_GREEN: str = _true_colors['JUNGLE_GREEN']
    KELLY_GREEN: str = _true_colors['KELLY_GREEN']
    KEPPEL: str = _true_colors['KEPPEL']
    KEY_LIME: str = _true_colors['KEY_LIME']
    KHAKI_WEB: str = _true_colors['KHAKI_WEB']
    KHAKI_X11_LIGHT_KHAKI: str = _true_colors['KHAKI_X11_LIGHT_KHAKI']
    KOBE: str = _true_colors['KOBE']
    KOBI: str = _true_colors['KOBI']
    KOBICHA: str = _true_colors['KOBICHA']
    KSU_PURPLE: str = _true_colors['KSU_PURPLE']
    LANGUID_LAVENDER: str = _true_colors['LANGUID_LAVENDER']
    LAPIS_LAZULI: str = _true_colors['LAPIS_LAZULI']
    LASER_LEMON: str = _true_colors['LASER_LEMON']
    LAUREL_GREEN: str = _true_colors['LAUREL_GREEN']
    LAVA: str = _true_colors['LAVA']
    LAVENDER_FLORAL: str = _true_colors['LAVENDER_FLORAL']
    LAVENDER_WEB: str = _true_colors['LAVENDER_WEB']
    LAVENDER_BLUE: str = _true_colors['LAVENDER_BLUE']
    LAVENDER_BLUSH: str = _true_colors['LAVENDER_BLUSH']
    LAVENDER_GRAY: str = _true_colors['LAVENDER_GRAY']
    LAWN_GREEN: str = _true_colors['LAWN_GREEN']
    LEMON: str = _true_colors['LEMON']
    LEMON_CHIFFON: str = _true_colors['LEMON_CHIFFON']
    LEMON_CURRY: str = _true_colors['LEMON_CURRY']
    LEMON_GLACIER: str = _true_colors['LEMON_GLACIER']
    LEMON_MERINGUE: str = _true_colors['LEMON_MERINGUE']
    LEMON_YELLOW: str = _true_colors['LEMON_YELLOW']
    LEMON_YELLOW_CRAYOLA: str = _true_colors['LEMON_YELLOW_CRAYOLA']
    LIBERTY: str = _true_colors['LIBERTY']
    LIGHT_BLUE: str = _true_colors['LIGHT_BLUE']
    LIGHT_CORAL: str = _true_colors['LIGHT_CORAL']
    LIGHT_CORNFLOWER_BLUE: str = _true_colors['LIGHT_CORNFLOWER_BLUE']
    LIGHT_CYAN: str = _true_colors['LIGHT_CYAN']
    LIGHT_FRENCH_BEIGE: str = _true_colors['LIGHT_FRENCH_BEIGE']
    LIGHT_GOLDENROD_YELLOW: str = _true_colors['LIGHT_GOLDENROD_YELLOW']
    LIGHT_GRAY: str = _true_colors['LIGHT_GRAY']
    LIGHT_GREEN: str = _true_colors['LIGHT_GREEN']
    LIGHT_ORANGE: str = _true_colors['LIGHT_ORANGE']
    LIGHT_PERIWINKLE: str = _true_colors['LIGHT_PERIWINKLE']
    LIGHT_PINK: str = _true_colors['LIGHT_PINK']
    LIGHT_SALMON: str = _true_colors['LIGHT_SALMON']
    LIGHT_SEA_GREEN: str = _true_colors['LIGHT_SEA_GREEN']
    LIGHT_SKY_BLUE: str = _true_colors['LIGHT_SKY_BLUE']
    LIGHT_SLATE_GRAY: str = _true_colors['LIGHT_SLATE_GRAY']
    LIGHT_STEEL_BLUE: str = _true_colors['LIGHT_STEEL_BLUE']
    LIGHT_YELLOW: str = _true_colors['LIGHT_YELLOW']
    LILAC: str = _true_colors['LILAC']
    LILAC_LUSTER: str = _true_colors['LILAC_LUSTER']
    LIME_COLOR_WHEEL: str = _true_colors['LIME_COLOR_WHEEL']
    LIME_WEB_X11_GREEN: str = _true_colors['LIME_WEB_X11_GREEN']
    LIME_GREEN: str = _true_colors['LIME_GREEN']
    LINCOLN_GREEN: str = _true_colors['LINCOLN_GREEN']
    LINEN: str = _true_colors['LINEN']
    LION: str = _true_colors['LION']
    LISERAN_PURPLE: str = _true_colors['LISERAN_PURPLE']
    LITTLE_BOY_BLUE: str = _true_colors['LITTLE_BOY_BLUE']
    LIVER: str = _true_colors['LIVER']
    LIVER_DOGS: str = _true_colors['LIVER_DOGS']
    LIVER_ORGAN: str = _true_colors['LIVER_ORGAN']
    LIVER_CHESTNUT: str = _true_colors['LIVER_CHESTNUT']
    LIVID: str = _true_colors['LIVID']
    MACARONI_AND_CHEESE: str = _true_colors['MACARONI_AND_CHEESE']
    MADDER_LAKE: str = _true_colors['MADDER_LAKE']
    MAGENTA_CRAYOLA: str = _true_colors['MAGENTA_CRAYOLA']
    MAGENTA_DYE: str = _true_colors['MAGENTA_DYE']
    MAGENTA_PANTONE: str = _true_colors['MAGENTA_PANTONE']
    MAGENTA_PROCESS: str = _true_colors['MAGENTA_PROCESS']
    MAGENTA_HAZE: str = _true_colors['MAGENTA_HAZE']
    MAGIC_MINT: str = _true_colors['MAGIC_MINT']
    MAGNOLIA: str = _true_colors['MAGNOLIA']
    MAHOGANY: str = _true_colors['MAHOGANY']
    MAIZE: str = _true_colors['MAIZE']
    MAIZE_CRAYOLA: str = _true_colors['MAIZE_CRAYOLA']
    MAJORELLE_BLUE: str = _true_colors['MAJORELLE_BLUE']
    MALACHITE: str = _true_colors['MALACHITE']
    MANATEE: str = _true_colors['MANATEE']
    MANDARIN: str = _true_colors['MANDARIN']
    MANGO: str = _true_colors['MANGO']
    MANGO_TANGO: str = _true_colors['MANGO_TANGO']
    MANTIS: str = _true_colors['MANTIS']
    MARDI_GRAS: str = _true_colors['MARDI_GRAS']
    MARIGOLD: str = _true_colors['MARIGOLD']
    MAROON_CRAYOLA: str = _true_colors['MAROON_CRAYOLA']
    MAROON_WEB: str = _true_colors['MAROON_WEB']
    MAROON_X11: str = _true_colors['MAROON_X11']
    MAUVE: str = _true_colors['MAUVE']
    MAUVE_TAUPE: str = _true_colors['MAUVE_TAUPE']
    MAUVELOUS: str = _true_colors['MAUVELOUS']
    MAXIMUM_BLUE: str = _true_colors['MAXIMUM_BLUE']
    MAXIMUM_BLUE_GREEN: str = _true_colors['MAXIMUM_BLUE_GREEN']
    MAXIMUM_BLUE_PURPLE: str = _true_colors['MAXIMUM_BLUE_PURPLE']
    MAXIMUM_GREEN: str = _true_colors['MAXIMUM_GREEN']
    MAXIMUM_GREEN_YELLOW: str = _true_colors['MAXIMUM_GREEN_YELLOW']
    MAXIMUM_PURPLE: str = _true_colors['MAXIMUM_PURPLE']
    MAXIMUM_RED: str = _true_colors['MAXIMUM_RED']
    MAXIMUM_RED_PURPLE: str = _true_colors['MAXIMUM_RED_PURPLE']
    MAXIMUM_YELLOW: str = _true_colors['MAXIMUM_YELLOW']
    MAXIMUM_YELLOW_RED: str = _true_colors['MAXIMUM_YELLOW_RED']
    MAY_GREEN: str = _true_colors['MAY_GREEN']
    MAYA_BLUE: str = _true_colors['MAYA_BLUE']
    MEDIUM_AQUAMARINE: str = _true_colors['MEDIUM_AQUAMARINE']
    MEDIUM_BLUE: str = _true_colors['MEDIUM_BLUE']
    MEDIUM_CANDY_APPLE_RED: str = _true_colors['MEDIUM_CANDY_APPLE_RED']
    MEDIUM_CARMINE: str = _true_colors['MEDIUM_CARMINE']
    MEDIUM_CHAMPAGNE: str = _true_colors['MEDIUM_CHAMPAGNE']
    MEDIUM_ORCHID: str = _true_colors['MEDIUM_ORCHID']
    MEDIUM_PURPLE: str = _true_colors['MEDIUM_PURPLE']
    MEDIUM_SEA_GREEN: str = _true_colors['MEDIUM_SEA_GREEN']
    MEDIUM_SLATE_BLUE: str = _true_colors['MEDIUM_SLATE_BLUE']
    MEDIUM_SPRING_GREEN: str = _true_colors['MEDIUM_SPRING_GREEN']
    MEDIUM_TURQUOISE: str = _true_colors['MEDIUM_TURQUOISE']
    MEDIUM_VIOLET_RED: str = _true_colors['MEDIUM_VIOLET_RED']
    MELLOW_APRICOT: str = _true_colors['MELLOW_APRICOT']
    MELLOW_YELLOW: str = _true_colors['MELLOW_YELLOW']
    MELON: str = _true_colors['MELON']
    METALLIC_GOLD: str = _true_colors['METALLIC_GOLD']
    METALLIC_SEAWEED: str = _true_colors['METALLIC_SEAWEED']
    METALLIC_SUNBURST: str = _true_colors['METALLIC_SUNBURST']
    MEXICAN_PINK: str = _true_colors['MEXICAN_PINK']
    MIDDLE_BLUE: str = _true_colors['MIDDLE_BLUE']
    MIDDLE_BLUE_GREEN: str = _true_colors['MIDDLE_BLUE_GREEN']
    MIDDLE_BLUE_PURPLE: str = _true_colors['MIDDLE_BLUE_PURPLE']
    MIDDLE_GREY: str = _true_colors['MIDDLE_GREY']
    MIDDLE_GREEN: str = _true_colors['MIDDLE_GREEN']
    MIDDLE_GREEN_YELLOW: str = _true_colors['MIDDLE_GREEN_YELLOW']
    MIDDLE_PURPLE: str = _true_colors['MIDDLE_PURPLE']
    MIDDLE_RED: str = _true_colors['MIDDLE_RED']
    MIDDLE_RED_PURPLE: str = _true_colors['MIDDLE_RED_PURPLE']
    MIDDLE_YELLOW: str = _true_colors['MIDDLE_YELLOW']
    MIDDLE_YELLOW_RED: str = _true_colors['MIDDLE_YELLOW_RED']
    MIDNIGHT: str = _true_colors['MIDNIGHT']
    MIDNIGHT_BLUE: str = _true_colors['MIDNIGHT_BLUE']
    MIDNIGHT_GREEN_EAGLE_GREEN: str = _true_colors['MIDNIGHT_GREEN_EAGLE_GREEN']
    MIKADO_YELLOW: str = _true_colors['MIKADO_YELLOW']
    MIMI_PINK: str = _true_colors['MIMI_PINK']
    MINDARO: str = _true_colors['MINDARO']
    MING: str = _true_colors['MING']
    MINION_YELLOW: str = _true_colors['MINION_YELLOW']
    MINT: str = _true_colors['MINT']
    MINT_CREAM: str = _true_colors['MINT_CREAM']
    MINT_GREEN: str = _true_colors['MINT_GREEN']
    MISTY_MOSS: str = _true_colors['MISTY_MOSS']
    MISTY_ROSE: str = _true_colors['MISTY_ROSE']
    MODE_BEIGE: str = _true_colors['MODE_BEIGE']
    MONA_LISA: str = _true_colors['MONA_LISA']
    MORNING_BLUE: str = _true_colors['MORNING_BLUE']
    MOSS_GREEN: str = _true_colors['MOSS_GREEN']
    MOUNTAIN_MEADOW: str = _true_colors['MOUNTAIN_MEADOW']
    MOUNTBATTEN_PINK: str = _true_colors['MOUNTBATTEN_PINK']
    MSU_GREEN: str = _true_colors['MSU_GREEN']
    MULBERRY: str = _true_colors['MULBERRY']
    MULBERRY_CRAYOLA: str = _true_colors['MULBERRY_CRAYOLA']
    MUSTARD: str = _true_colors['MUSTARD']
    MYRTLE_GREEN: str = _true_colors['MYRTLE_GREEN']
    MYSTIC: str = _true_colors['MYSTIC']
    MYSTIC_MAROON: str = _true_colors['MYSTIC_MAROON']
    NADESHIKO_PINK: str = _true_colors['NADESHIKO_PINK']
    NAPLES_YELLOW: str = _true_colors['NAPLES_YELLOW']
    NAVAJO_WHITE: str = _true_colors['NAVAJO_WHITE']
    NAVY_BLUE: str = _true_colors['NAVY_BLUE']
    NAVY_BLUE_CRAYOLA: str = _true_colors['NAVY_BLUE_CRAYOLA']
    NEON_BLUE: str = _true_colors['NEON_BLUE']
    NEON_GREEN: str = _true_colors['NEON_GREEN']
    NEON_FUCHSIA: str = _true_colors['NEON_FUCHSIA']
    NEW_CAR: str = _true_colors['NEW_CAR']
    NEW_YORK_PINK: str = _true_colors['NEW_YORK_PINK']
    NICKEL: str = _true_colors['NICKEL']
    NON_PHOTO_BLUE: str = _true_colors['NON_PHOTO_BLUE']
    NYANZA: str = _true_colors['NYANZA']
    OCHRE: str = _true_colors['OCHRE']
    OLD_BURGUNDY: str = _true_colors['OLD_BURGUNDY']
    OLD_GOLD: str = _true_colors['OLD_GOLD']
    OLD_LACE: str = _true_colors['OLD_LACE']
    OLD_LAVENDER: str = _true_colors['OLD_LAVENDER']
    OLD_MAUVE: str = _true_colors['OLD_MAUVE']
    OLD_ROSE: str = _true_colors['OLD_ROSE']
    OLD_SILVER: str = _true_colors['OLD_SILVER']
    OLIVE: str = _true_colors['OLIVE']
    OLIVE_DRAB_3: str = _true_colors['OLIVE_DRAB_3']
    OLIVE_DRAB_7: str = _true_colors['OLIVE_DRAB_7']
    OLIVE_GREEN: str = _true_colors['OLIVE_GREEN']
    OLIVINE: str = _true_colors['OLIVINE']
    ONYX: str = _true_colors['ONYX']
    OPAL: str = _true_colors['OPAL']
    OPERA_MAUVE: str = _true_colors['OPERA_MAUVE']
    ORANGE: str = _true_colors['ORANGE']
    ORANGE_CRAYOLA: str = _true_colors['ORANGE_CRAYOLA']
    ORANGE_PANTONE: str = _true_colors['ORANGE_PANTONE']
    ORANGE_WEB: str = _true_colors['ORANGE_WEB']
    ORANGE_PEEL: str = _true_colors['ORANGE_PEEL']
    ORANGE_RED: str = _true_colors['ORANGE_RED']
    ORANGE_RED_CRAYOLA: str = _true_colors['ORANGE_RED_CRAYOLA']
    ORANGE_SODA: str = _true_colors['ORANGE_SODA']
    ORANGE_YELLOW: str = _true_colors['ORANGE_YELLOW']
    ORANGE_YELLOW_CRAYOLA: str = _true_colors['ORANGE_YELLOW_CRAYOLA']
    ORCHID: str = _true_colors['ORCHID']
    ORCHID_PINK: str = _true_colors['ORCHID_PINK']
    ORCHID_CRAYOLA: str = _true_colors['ORCHID_CRAYOLA']
    OUTER_SPACE_CRAYOLA: str = _true_colors['OUTER_SPACE_CRAYOLA']
    OUTRAGEOUS_ORANGE: str = _true_colors['OUTRAGEOUS_ORANGE']
    OXBLOOD: str = _true_colors['OXBLOOD']
    OXFORD_BLUE: str = _true_colors['OXFORD_BLUE']
    OU_CRIMSON_RED: str = _true_colors['OU_CRIMSON_RED']
    PACIFIC_BLUE: str = _true_colors['PACIFIC_BLUE']
    PAKISTAN_GREEN: str = _true_colors['PAKISTAN_GREEN']
    PALATINATE_PURPLE: str = _true_colors['PALATINATE_PURPLE']
    PALE_AQUA: str = _true_colors['PALE_AQUA']
    PALE_CERULEAN: str = _true_colors['PALE_CERULEAN']
    PALE_DOGWOOD: str = _true_colors['PALE_DOGWOOD']
    PALE_PINK: str = _true_colors['PALE_PINK']
    PALE_PURPLE_PANTONE: str = _true_colors['PALE_PURPLE_PANTONE']
    PALE_SPRING_BUD: str = _true_colors['PALE_SPRING_BUD']
    PANSY_PURPLE: str = _true_colors['PANSY_PURPLE']
    PAOLO_VERONESE_GREEN: str = _true_colors['PAOLO_VERONESE_GREEN']
    PAPAYA_WHIP: str = _true_colors['PAPAYA_WHIP']
    PARADISE_PINK: str = _true_colors['PARADISE_PINK']
    PARCHMENT: str = _true_colors['PARCHMENT']
    PARIS_GREEN: str = _true_colors['PARIS_GREEN']
    PASTEL_PINK: str = _true_colors['PASTEL_PINK']
    PATRIARCH: str = _true_colors['PATRIARCH']
    PAUA: str = _true_colors['PAUA']
    PAYNE_S_GREY: str = _true_colors['PAYNE_S_GREY']
    PEACH: str = _true_colors['PEACH']
    PEACH_CRAYOLA: str = _true_colors['PEACH_CRAYOLA']
    PEACH_PUFF: str = _true_colors['PEACH_PUFF']
    PEAR: str = _true_colors['PEAR']
    PEARLY_PURPLE: str = _true_colors['PEARLY_PURPLE']
    PERIWINKLE: str = _true_colors['PERIWINKLE']
    PERIWINKLE_CRAYOLA: str = _true_colors['PERIWINKLE_CRAYOLA']
    PERMANENT_GERANIUM_LAKE: str = _true_colors['PERMANENT_GERANIUM_LAKE']
    PERSIAN_BLUE: str = _true_colors['PERSIAN_BLUE']
    PERSIAN_GREEN: str = _true_colors['PERSIAN_GREEN']
    PERSIAN_INDIGO: str = _true_colors['PERSIAN_INDIGO']
    PERSIAN_ORANGE: str = _true_colors['PERSIAN_ORANGE']
    PERSIAN_PINK: str = _true_colors['PERSIAN_PINK']
    PERSIAN_PLUM: str = _true_colors['PERSIAN_PLUM']
    PERSIAN_RED: str = _true_colors['PERSIAN_RED']
    PERSIAN_ROSE: str = _true_colors['PERSIAN_ROSE']
    PERSIMMON: str = _true_colors['PERSIMMON']
    PEWTER_BLUE: str = _true_colors['PEWTER_BLUE']
    PHLOX: str = _true_colors['PHLOX']
    PHTHALO_BLUE: str = _true_colors['PHTHALO_BLUE']
    PHTHALO_GREEN: str = _true_colors['PHTHALO_GREEN']
    PICOTEE_BLUE: str = _true_colors['PICOTEE_BLUE']
    PICTORIAL_CARMINE: str = _true_colors['PICTORIAL_CARMINE']
    PIGGY_PINK: str = _true_colors['PIGGY_PINK']
    PINE_GREEN: str = _true_colors['PINE_GREEN']
    PINK: str = _true_colors['PINK']
    PINK_PANTONE: str = _true_colors['PINK_PANTONE']
    PINK_LACE: str = _true_colors['PINK_LACE']
    PINK_LAVENDER: str = _true_colors['PINK_LAVENDER']
    PINK_SHERBET: str = _true_colors['PINK_SHERBET']
    PISTACHIO: str = _true_colors['PISTACHIO']
    PLATINUM: str = _true_colors['PLATINUM']
    PLUM: str = _true_colors['PLUM']
    PLUM_WEB: str = _true_colors['PLUM_WEB']
    PLUMP_PURPLE: str = _true_colors['PLUMP_PURPLE']
    POLISHED_PINE: str = _true_colors['POLISHED_PINE']
    POMP_AND_POWER: str = _true_colors['POMP_AND_POWER']
    POPSTAR: str = _true_colors['POPSTAR']
    PORTLAND_ORANGE: str = _true_colors['PORTLAND_ORANGE']
    POWDER_BLUE: str = _true_colors['POWDER_BLUE']
    PRAIRIE_GOLD: str = _true_colors['PRAIRIE_GOLD']
    PRINCETON_ORANGE: str = _true_colors['PRINCETON_ORANGE']
    PRUNE: str = _true_colors['PRUNE']
    PRUSSIAN_BLUE: str = _true_colors['PRUSSIAN_BLUE']
    PSYCHEDELIC_PURPLE: str = _true_colors['PSYCHEDELIC_PURPLE']
    PUCE: str = _true_colors['PUCE']
    PULLMAN_BROWN_UPS_BROWN: str = _true_colors['PULLMAN_BROWN_UPS_BROWN']
    PUMPKIN: str = _true_colors['PUMPKIN']
    PURPLE: str = _true_colors['PURPLE']
    PURPLE_WEB: str = _true_colors['PURPLE_WEB']
    PURPLE_MUNSELL: str = _true_colors['PURPLE_MUNSELL']
    PURPLE_X11: str = _true_colors['PURPLE_X11']
    PURPLE_MOUNTAIN_MAJESTY: str = _true_colors['PURPLE_MOUNTAIN_MAJESTY']
    PURPLE_NAVY: str = _true_colors['PURPLE_NAVY']
    PURPLE_PIZZAZZ: str = _true_colors['PURPLE_PIZZAZZ']
    PURPLE_PLUM: str = _true_colors['PURPLE_PLUM']
    PURPUREUS: str = _true_colors['PURPUREUS']
    QUEEN_BLUE: str = _true_colors['QUEEN_BLUE']
    QUEEN_PINK: str = _true_colors['QUEEN_PINK']
    QUICK_SILVER: str = _true_colors['QUICK_SILVER']
    QUINACRIDONE_MAGENTA: str = _true_colors['QUINACRIDONE_MAGENTA']
    RADICAL_RED: str = _true_colors['RADICAL_RED']
    RAISIN_BLACK: str = _true_colors['RAISIN_BLACK']
    RAJAH: str = _true_colors['RAJAH']
    RASPBERRY: str = _true_colors['RASPBERRY']
    RASPBERRY_GLACE: str = _true_colors['RASPBERRY_GLACE']
    RASPBERRY_ROSE: str = _true_colors['RASPBERRY_ROSE']
    RAW_SIENNA: str = _true_colors['RAW_SIENNA']
    RAW_UMBER: str = _true_colors['RAW_UMBER']
    RAZZLE_DAZZLE_ROSE: str = _true_colors['RAZZLE_DAZZLE_ROSE']
    RAZZMATAZZ: str = _true_colors['RAZZMATAZZ']
    RAZZMIC_BERRY: str = _true_colors['RAZZMIC_BERRY']
    REBECCA_PURPLE: str = _true_colors['REBECCA_PURPLE']
    RED_CRAYOLA: str = _true_colors['RED_CRAYOLA']
    RED_MUNSELL: str = _true_colors['RED_MUNSELL']
    RED_NCS: str = _true_colors['RED_NCS']
    RED_PANTONE: str = _true_colors['RED_PANTONE']
    RED_PIGMENT: str = _true_colors['RED_PIGMENT']
    RED_RYB: str = _true_colors['RED_RYB']
    RED_ORANGE: str = _true_colors['RED_ORANGE']
    RED_ORANGE_CRAYOLA: str = _true_colors['RED_ORANGE_CRAYOLA']
    RED_ORANGE_COLOR_WHEEL: str = _true_colors['RED_ORANGE_COLOR_WHEEL']
    RED_PURPLE: str = _true_colors['RED_PURPLE']
    RED_SALSA: str = _true_colors['RED_SALSA']
    RED_VIOLET: str = _true_colors['RED_VIOLET']
    RED_VIOLET_CRAYOLA: str = _true_colors['RED_VIOLET_CRAYOLA']
    RED_VIOLET_COLOR_WHEEL: str = _true_colors['RED_VIOLET_COLOR_WHEEL']
    REDWOOD: str = _true_colors['REDWOOD']
    RESOLUTION_BLUE: str = _true_colors['RESOLUTION_BLUE']
    RHYTHM: str = _true_colors['RHYTHM']
    RICH_BLACK: str = _true_colors['RICH_BLACK']
    RICH_BLACK_FOGRA29: str = _true_colors['RICH_BLACK_FOGRA29']
    RICH_BLACK_FOGRA39: str = _true_colors['RICH_BLACK_FOGRA39']
    RIFLE_GREEN: str = _true_colors['RIFLE_GREEN']
    ROBIN_EGG_BLUE: str = _true_colors['ROBIN_EGG_BLUE']
    ROCKET_METALLIC: str = _true_colors['ROCKET_METALLIC']
    ROJO_SPANISH_RED: str = _true_colors['ROJO_SPANISH_RED']
    ROMAN_SILVER: str = _true_colors['ROMAN_SILVER']
    ROSE: str = _true_colors['ROSE']
    ROSE_BONBON: str = _true_colors['ROSE_BONBON']
    ROSE_DUST: str = _true_colors['ROSE_DUST']
    ROSE_EBONY: str = _true_colors['ROSE_EBONY']
    ROSE_MADDER: str = _true_colors['ROSE_MADDER']
    ROSE_PINK: str = _true_colors['ROSE_PINK']
    ROSE_POMPADOUR: str = _true_colors['ROSE_POMPADOUR']
    ROSE_RED: str = _true_colors['ROSE_RED']
    ROSE_TAUPE: str = _true_colors['ROSE_TAUPE']
    ROSE_VALE: str = _true_colors['ROSE_VALE']
    ROSEWOOD: str = _true_colors['ROSEWOOD']
    ROSSO_CORSA: str = _true_colors['ROSSO_CORSA']
    ROSY_BROWN: str = _true_colors['ROSY_BROWN']
    ROYAL_BLUE_DARK: str = _true_colors['ROYAL_BLUE_DARK']
    ROYAL_BLUE_LIGHT: str = _true_colors['ROYAL_BLUE_LIGHT']
    ROYAL_PURPLE: str = _true_colors['ROYAL_PURPLE']
    ROYAL_YELLOW: str = _true_colors['ROYAL_YELLOW']
    RUBER: str = _true_colors['RUBER']
    RUBINE_RED: str = _true_colors['RUBINE_RED']
    RUBY: str = _true_colors['RUBY']
    RUBY_RED: str = _true_colors['RUBY_RED']
    RUFOUS: str = _true_colors['RUFOUS']
    RUSSET: str = _true_colors['RUSSET']
    RUSSIAN_GREEN: str = _true_colors['RUSSIAN_GREEN']
    RUSSIAN_VIOLET: str = _true_colors['RUSSIAN_VIOLET']
    RUST: str = _true_colors['RUST']
    RUSTY_RED: str = _true_colors['RUSTY_RED']
    SACRAMENTO_STATE_GREEN: str = _true_colors['SACRAMENTO_STATE_GREEN']
    SADDLE_BROWN: str = _true_colors['SADDLE_BROWN']
    SAFETY_ORANGE: str = _true_colors['SAFETY_ORANGE']
    SAFETY_ORANGE_BLAZE_ORANGE: str = _true_colors['SAFETY_ORANGE_BLAZE_ORANGE']
    SAFETY_YELLOW: str = _true_colors['SAFETY_YELLOW']
    SAFFRON: str = _true_colors['SAFFRON']
    SAGE: str = _true_colors['SAGE']
    ST_PATRICK_S_BLUE: str = _true_colors['ST_PATRICK_S_BLUE']
    SALMON: str = _true_colors['SALMON']
    SALMON_PINK: str = _true_colors['SALMON_PINK']
    SAND: str = _true_colors['SAND']
    SAND_DUNE: str = _true_colors['SAND_DUNE']
    SANDY_BROWN: str = _true_colors['SANDY_BROWN']
    SAP_GREEN: str = _true_colors['SAP_GREEN']
    SAPPHIRE: str = _true_colors['SAPPHIRE']
    SAPPHIRE_BLUE: str = _true_colors['SAPPHIRE_BLUE']
    SAPPHIRE_CRAYOLA: str = _true_colors['SAPPHIRE_CRAYOLA']
    SATIN_SHEEN_GOLD: str = _true_colors['SATIN_SHEEN_GOLD']
    SCARLET: str = _true_colors['SCARLET']
    SCHAUSS_PINK: str = _true_colors['SCHAUSS_PINK']
    SCHOOL_BUS_YELLOW: str = _true_colors['SCHOOL_BUS_YELLOW']
    SCREAMIN_GREEN: str = _true_colors['SCREAMIN_GREEN']
    SEA_GREEN: str = _true_colors['SEA_GREEN']
    SEA_GREEN_CRAYOLA: str = _true_colors['SEA_GREEN_CRAYOLA']
    SEANCE: str = _true_colors['SEANCE']
    SEAL_BROWN: str = _true_colors['SEAL_BROWN']
    SEASHELL: str = _true_colors['SEASHELL']
    SECRET: str = _true_colors['SECRET']
    SELECTIVE_YELLOW: str = _true_colors['SELECTIVE_YELLOW']
    SEPIA: str = _true_colors['SEPIA']
    SHADOW: str = _true_colors['SHADOW']
    SHADOW_BLUE: str = _true_colors['SHADOW_BLUE']
    SHAMROCK_GREEN: str = _true_colors['SHAMROCK_GREEN']
    SHEEN_GREEN: str = _true_colors['SHEEN_GREEN']
    SHIMMERING_BLUSH: str = _true_colors['SHIMMERING_BLUSH']
    SHINY_SHAMROCK: str = _true_colors['SHINY_SHAMROCK']
    SHOCKING_PINK: str = _true_colors['SHOCKING_PINK']
    SHOCKING_PINK_CRAYOLA: str = _true_colors['SHOCKING_PINK_CRAYOLA']
    SIENNA: str = _true_colors['SIENNA']
    SILVER: str = _true_colors['SILVER']
    SILVER_CRAYOLA: str = _true_colors['SILVER_CRAYOLA']
    SILVER_METALLIC: str = _true_colors['SILVER_METALLIC']
    SILVER_CHALICE: str = _true_colors['SILVER_CHALICE']
    SILVER_PINK: str = _true_colors['SILVER_PINK']
    SILVER_SAND: str = _true_colors['SILVER_SAND']
    SINOPIA: str = _true_colors['SINOPIA']
    SIZZLING_RED: str = _true_colors['SIZZLING_RED']
    SIZZLING_SUNRISE: str = _true_colors['SIZZLING_SUNRISE']
    SKOBELOFF: str = _true_colors['SKOBELOFF']
    SKY_BLUE: str = _true_colors['SKY_BLUE']
    SKY_BLUE_CRAYOLA: str = _true_colors['SKY_BLUE_CRAYOLA']
    SKY_MAGENTA: str = _true_colors['SKY_MAGENTA']
    SLATE_BLUE: str = _true_colors['SLATE_BLUE']
    SLATE_GRAY: str = _true_colors['SLATE_GRAY']
    SLIMY_GREEN: str = _true_colors['SLIMY_GREEN']
    SMITTEN: str = _true_colors['SMITTEN']
    SMOKY_BLACK: str = _true_colors['SMOKY_BLACK']
    SNOW: str = _true_colors['SNOW']
    SOLID_PINK: str = _true_colors['SOLID_PINK']
    SONIC_SILVER: str = _true_colors['SONIC_SILVER']
    SPACE_CADET: str = _true_colors['SPACE_CADET']
    SPANISH_BISTRE: str = _true_colors['SPANISH_BISTRE']
    SPANISH_BLUE: str = _true_colors['SPANISH_BLUE']
    SPANISH_CARMINE: str = _true_colors['SPANISH_CARMINE']
    SPANISH_GRAY: str = _true_colors['SPANISH_GRAY']
    SPANISH_GREEN: str = _true_colors['SPANISH_GREEN']
    SPANISH_ORANGE: str = _true_colors['SPANISH_ORANGE']
    SPANISH_PINK: str = _true_colors['SPANISH_PINK']
    SPANISH_RED: str = _true_colors['SPANISH_RED']
    SPANISH_SKY_BLUE: str = _true_colors['SPANISH_SKY_BLUE']
    SPANISH_VIOLET: str = _true_colors['SPANISH_VIOLET']
    SPANISH_VIRIDIAN: str = _true_colors['SPANISH_VIRIDIAN']
    SPRING_BUD: str = _true_colors['SPRING_BUD']
    SPRING_FROST: str = _true_colors['SPRING_FROST']
    SPRING_GREEN: str = _true_colors['SPRING_GREEN']
    SPRING_GREEN_CRAYOLA: str = _true_colors['SPRING_GREEN_CRAYOLA']
    STAR_COMMAND_BLUE: str = _true_colors['STAR_COMMAND_BLUE']
    STEEL_BLUE: str = _true_colors['STEEL_BLUE']
    STEEL_PINK: str = _true_colors['STEEL_PINK']
    STIL_DE_GRAIN_YELLOW: str = _true_colors['STIL_DE_GRAIN_YELLOW']
    STIZZA: str = _true_colors['STIZZA']
    STRAW: str = _true_colors['STRAW']
    STRAWBERRY: str = _true_colors['STRAWBERRY']
    STRAWBERRY_BLONDE: str = _true_colors['STRAWBERRY_BLONDE']
    STRONG_LIME_GREEN: str = _true_colors['STRONG_LIME_GREEN']
    SUGAR_PLUM: str = _true_colors['SUGAR_PLUM']
    SUNGLOW: str = _true_colors['SUNGLOW']
    SUNRAY: str = _true_colors['SUNRAY']
    SUNSET: str = _true_colors['SUNSET']
    SUPER_PINK: str = _true_colors['SUPER_PINK']
    SWEET_BROWN: str = _true_colors['SWEET_BROWN']
    SYRACUSE_ORANGE: str = _true_colors['SYRACUSE_ORANGE']
    TAN: str = _true_colors['TAN']
    TAN_CRAYOLA: str = _true_colors['TAN_CRAYOLA']
    TANGERINE: str = _true_colors['TANGERINE']
    TANGO_PINK: str = _true_colors['TANGO_PINK']
    TART_ORANGE: str = _true_colors['TART_ORANGE']
    TAUPE: str = _true_colors['TAUPE']
    TAUPE_GRAY: str = _true_colors['TAUPE_GRAY']
    TEA_GREEN: str = _true_colors['TEA_GREEN']
    TEA_ROSE: str = _true_colors['TEA_ROSE']
    TEAL: str = _true_colors['TEAL']
    TEAL_BLUE: str = _true_colors['TEAL_BLUE']
    TECHNOBOTANICA: str = _true_colors['TECHNOBOTANICA']
    TELEMAGENTA: str = _true_colors['TELEMAGENTA']
    TENNE_TAWNY: str = _true_colors['TENNE_TAWNY']
    TERRA_COTTA: str = _true_colors['TERRA_COTTA']
    THISTLE: str = _true_colors['THISTLE']
    THULIAN_PINK: str = _true_colors['THULIAN_PINK']
    TICKLE_ME_PINK: str = _true_colors['TICKLE_ME_PINK']
    TIFFANY_BLUE: str = _true_colors['TIFFANY_BLUE']
    TIMBERWOLF: str = _true_colors['TIMBERWOLF']
    TITANIUM_YELLOW: str = _true_colors['TITANIUM_YELLOW']
    TOMATO: str = _true_colors['TOMATO']
    TOURMALINE: str = _true_colors['TOURMALINE']
    TROPICAL_RAINFOREST: str = _true_colors['TROPICAL_RAINFOREST']
    TRUE_BLUE: str = _true_colors['TRUE_BLUE']
    TRYPAN_BLUE: str = _true_colors['TRYPAN_BLUE']
    TUFTS_BLUE: str = _true_colors['TUFTS_BLUE']
    TUMBLEWEED: str = _true_colors['TUMBLEWEED']
    TURQUOISE: str = _true_colors['TURQUOISE']
    TURQUOISE_BLUE: str = _true_colors['TURQUOISE_BLUE']
    TURQUOISE_GREEN: str = _true_colors['TURQUOISE_GREEN']
    TURTLE_GREEN: str = _true_colors['TURTLE_GREEN']
    TUSCAN: str = _true_colors['TUSCAN']
    TUSCAN_BROWN: str = _true_colors['TUSCAN_BROWN']
    TUSCAN_RED: str = _true_colors['TUSCAN_RED']
    TUSCAN_TAN: str = _true_colors['TUSCAN_TAN']
    TUSCANY: str = _true_colors['TUSCANY']
    TWILIGHT_LAVENDER: str = _true_colors['TWILIGHT_LAVENDER']
    TYRIAN_PURPLE: str = _true_colors['TYRIAN_PURPLE']
    UA_BLUE: str = _true_colors['UA_BLUE']
    UA_RED: str = _true_colors['UA_RED']
    ULTRAMARINE: str = _true_colors['ULTRAMARINE']
    ULTRAMARINE_BLUE: str = _true_colors['ULTRAMARINE_BLUE']
    ULTRA_PINK: str = _true_colors['ULTRA_PINK']
    ULTRA_RED: str = _true_colors['ULTRA_RED']
    UMBER: str = _true_colors['UMBER']
    UNBLEACHED_SILK: str = _true_colors['UNBLEACHED_SILK']
    UNITED_NATIONS_BLUE: str = _true_colors['UNITED_NATIONS_BLUE']
    UNIVERSITY_OF_PENNSYLVANIA_RED: str = _true_colors['UNIVERSITY_OF_PENNSYLVANIA_RED']
    UNMELLOW_YELLOW: str = _true_colors['UNMELLOW_YELLOW']
    UP_FOREST_GREEN: str = _true_colors['UP_FOREST_GREEN']
    UP_MAROON: str = _true_colors['UP_MAROON']
    UPSDELL_RED: str = _true_colors['UPSDELL_RED']
    URANIAN_BLUE: str = _true_colors['URANIAN_BLUE']
    USAFA_BLUE: str = _true_colors['USAFA_BLUE']
    VAN_DYKE_BROWN: str = _true_colors['VAN_DYKE_BROWN']
    VANILLA: str = _true_colors['VANILLA']
    VANILLA_ICE: str = _true_colors['VANILLA_ICE']
    VEGAS_GOLD: str = _true_colors['VEGAS_GOLD']
    VENETIAN_RED: str = _true_colors['VENETIAN_RED']
    VERDIGRIS: str = _true_colors['VERDIGRIS']
    VERMILION: str = _true_colors['VERMILION']
    VERONICA: str = _true_colors['VERONICA']
    VIOLET: str = _true_colors['VIOLET']
    VIOLET_COLOR_WHEEL: str = _true_colors['VIOLET_COLOR_WHEEL']
    VIOLET_CRAYOLA: str = _true_colors['VIOLET_CRAYOLA']
    VIOLET_RYB: str = _true_colors['VIOLET_RYB']
    VIOLET_WEB: str = _true_colors['VIOLET_WEB']
    VIOLET_BLUE: str = _true_colors['VIOLET_BLUE']
    VIOLET_BLUE_CRAYOLA: str = _true_colors['VIOLET_BLUE_CRAYOLA']
    VIOLET_RED: str = _true_colors['VIOLET_RED']
    VIOLET_REDPERBANG: str = _true_colors['VIOLET_REDPERBANG']
    VIRIDIAN: str = _true_colors['VIRIDIAN']
    VIRIDIAN_GREEN: str = _true_colors['VIRIDIAN_GREEN']
    VIVID_BURGUNDY: str = _true_colors['VIVID_BURGUNDY']
    VIVID_SKY_BLUE: str = _true_colors['VIVID_SKY_BLUE']
    VIVID_TANGERINE: str = _true_colors['VIVID_TANGERINE']
    VIVID_VIOLET: str = _true_colors['VIVID_VIOLET']
    VOLT: str = _true_colors['VOLT']
    WARM_BLACK: str = _true_colors['WARM_BLACK']
    WEEZY_BLUE: str = _true_colors['WEEZY_BLUE']
    WHEAT: str = _true_colors['WHEAT']
    WILD_BLUE_YONDER: str = _true_colors['WILD_BLUE_YONDER']
    WILD_ORCHID: str = _true_colors['WILD_ORCHID']
    WILD_STRAWBERRY: str = _true_colors['WILD_STRAWBERRY']
    WILD_WATERMELON: str = _true_colors['WILD_WATERMELON']
    WINDSOR_TAN: str = _true_colors['WINDSOR_TAN']
    WINE: str = _true_colors['WINE']
    WINE_DREGS: str = _true_colors['WINE_DREGS']
    WINTER_SKY: str = _true_colors['WINTER_SKY']
    WINTERGREEN_DREAM: str = _true_colors['WINTERGREEN_DREAM']
    WISTERIA: str = _true_colors['WISTERIA']
    WOOD_BROWN: str = _true_colors['WOOD_BROWN']
    XANADU: str = _true_colors['XANADU']
    XANTHIC: str = _true_colors['XANTHIC']
    XANTHOUS: str = _true_colors['XANTHOUS']
    YALE_BLUE: str = _true_colors['YALE_BLUE']
    YELLOW_CRAYOLA: str = _true_colors['YELLOW_CRAYOLA']
    YELLOW_MUNSELL: str = _true_colors['YELLOW_MUNSELL']
    YELLOW_NCS: str = _true_colors['YELLOW_NCS']
    YELLOW_PANTONE: str = _true_colors['YELLOW_PANTONE']
    YELLOW_PROCESS: str = _true_colors['YELLOW_PROCESS']
    YELLOW_RYB: str = _true_colors['YELLOW_RYB']
    YELLOW_GREEN: str = _true_colors['YELLOW_GREEN']
    YELLOW_GREEN_CRAYOLA: str = _true_colors['YELLOW_GREEN_CRAYOLA']
    YELLOW_GREEN_COLOR_WHEEL: str = _true_colors['YELLOW_GREEN_COLOR_WHEEL']
    YELLOW_ORANGE: str = _true_colors['YELLOW_ORANGE']
    YELLOW_ORANGE_COLOR_WHEEL: str = _true_colors['YELLOW_ORANGE_COLOR_WHEEL']
    YELLOW_SUNSHINE: str = _true_colors['YELLOW_SUNSHINE']
    YINMN_BLUE: str = _true_colors['YINMN_BLUE']
    ZAFFRE: str = _true_colors['ZAFFRE']
    ZINNWALDITE_BROWN: str = _true_colors['ZINNWALDITE_BROWN']
    ZOMP: str = _true_colors['ZOMP']

    @classmethod
    def add_color(cls, name: str, ansi_code: str, true_color: Optional[bool] = True) -> None:
        """
        Enables the addition of a custom foreground color to the dictionary, supporting both standard
        and true color formats. However, it's essential to note that true colors can only be added if
        the terminal supports them.
        :param name: The name for the custom foreground color.
        :type name: str
        :param ansi_code: The ANSI code color value for the custom foreground.
        :type ansi_code: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(ansi_code, str, 'ansi_code should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')
        Validate.validate_ansi(ansi_code)

        if true_color and not is_true_color_supported():
            raise Warning('True colors are not supported by this terminal.')

        code = ansi_code[2:].rstrip('m')
        if true_color:
            pattern = (
                rf'^{Layer.Foreground.value};2;'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5]);'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5]);'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5])$'
            )
            if not re.match(pattern, code):
                raise ValueError('Unsupported ANSI code format.')

            cls._true_colors[name.upper()] = ansi_code
        else:
            if not code.isdigit():
                raise ValueError('Unsupported ANSI code format.')

            cls._standard_colors[name.upper()] = ansi_code

    @classmethod
    def get_colors(cls, true_color: Optional[bool] = True) -> dict:
        """
        Generates a dictionary containing a list of all colors based on the provided input.
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The dictionary containing the list of colors based on the provided input.
        :rtype: dict
        """
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            return dict(sorted(cls._true_colors.items()))
        else:
            return dict(sorted(cls._standard_colors.items()))

    @classmethod
    def get_color(cls, name: str, true_color: Optional[bool] = True) -> str:
        """
        Obtains the color code corresponding to the provided input.
        :param name: The name of the color to retrieve.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The color code value of the provided color name.
        :rtype: str
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            result = cls._true_colors.get(name.upper())
        else:
            result = cls._standard_colors.get(name.upper())

        if result is None:
            raise ValueError(
                f'{name} is not a valid {"true" if true_color else "standard"} '
                f'color value for TextColor'
            )

        return result

    @classmethod
    def is_standard_color(cls, name: str) -> bool:
        """
        Checks whether the provided color name corresponds to a standard color.
        :param name: The name of the color to be validated.
        :type name: str
        :return: True if the provided color is a standard color, False otherwise.
        :rtype: bool
        """
        return cls.is_valid_color(name, true_color=False)

    @classmethod
    def is_true_color(cls, name: str) -> bool:
        """
        Checks whether the provided color name corresponds to a true color.
        :param name: The name of the color to be validated.
        :type name: str
        :return: True if the provided color is a true color, False otherwise.
        :rtype: bool
        """
        return cls.is_valid_color(name, true_color=True)

    @classmethod
    def is_valid_color(cls, name: str, true_color: Optional[bool] = True) -> bool:
        """
        Checks whether the provided color name corresponds to either a standard or true color.
        :param name: The name of the color to be validated.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :return: True if the provided color is either a standard or true color, False otherwise.
        :rtype: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        try:
            return cls.get_color(name, true_color) is not None
        except ValueError:
            return False

    @classmethod
    def remove_color(cls, name: str, true_color: Optional[bool] = True) -> None:
        """
        Deletes the custom foreground color specified by name from the dictionary.
        :param name: The name of the color to be removed.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            if name.upper() in cls._true_colors:
                del cls._true_colors[name.upper()]
        else:
            if name.upper() in cls._standard_colors:
                del cls._standard_colors[name.upper()]


class TextEffect:
    """
    This class defines text effects for styling console text within the terminal. Additionally, the class offers
    methods to handle custom effects.
    """

    # Standard terminal effects supported by various operating systems
    _effects = {
        'BOLD': "\033[1m",
        'ITALIC': "\033[3m",
        'MONOSPACE': "\033[7m",
        'STRIKETHROUGH': "\033[9m",
        'UNDERLINE': "\033[4m"
    }

    # Constants defining effect values
    BOLD: str = _effects['BOLD']
    ITALIC: str = _effects['ITALIC']
    MONOSPACE: str = _effects['MONOSPACE']
    STRIKETHROUGH: str = _effects['STRIKETHROUGH']
    UNDERLINE: str = _effects['UNDERLINE']

    @classmethod
    def add_effect(cls, name: str, ansi_code: str) -> None:
        """
        Enables the addition of a custom effect to the dictionary.
        :param name: The name for the custom effect.
        :type name: str
        :param ansi_code: The ANSI code value for the custom effect.
        :type ansi_code: str
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(ansi_code, str, 'ansi_code should be a string.')
        Validate.validate_ansi(ansi_code)

        code = ansi_code[2:].rstrip('m')
        if not code.isdigit():
            raise ValueError('Unsupported ANSI code format.')

        cls._effects[name.upper()] = ansi_code

    @classmethod
    def get_effects(cls) -> dict:
        """
        Generates a dictionary containing a list of all effects.
        :return: The dictionary containing the list of effects.
        :rtype: dict
        """
        return dict(sorted(cls._effects.items()))

    @classmethod
    def get_effect(cls, name: str) -> str:
        """
        Obtains the effect code corresponding to the provided input.
        :param name: The name of the effect to retrieve.
        :type name: str
        :return: The color code value of the provided color name.
        :rtype: str
        """
        Validate.validate_type(name, str, 'name should be a string.')
        result = cls._effects.get(name.upper())

        if result is None:
            raise ValueError(
                f'{name} is not a valid effect value for TextEffect'
            )

        return result

    @classmethod
    def is_valid_effect(cls, name: str) -> bool:
        """
        Checks whether the provided effect name exists within the dictionary.
        :param name: The name of the effect to be validated.
        :type name: str
        :return: True if the provided effect exists, False otherwise.
        :rtype: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')

        try:
            return cls.get_effect(name) is not None
        except ValueError:
            return False

    @classmethod
    def remove_effect(cls, name: str) -> None:
        """
        Deletes the custom effect specified by name from the dictionary.
        :param name: The name of the effect to be removed.
        :type name: str
        """
        Validate.validate_type(name, str, 'name should be a string.')

        if name.upper() in cls._effects:
            del cls._effects[name.upper()]


class TextCase:
    """
    This class defines text cases for styling console text within the terminal.
    """

    # Standard terminal cases supported by various operating systems
    _cases = {
        'NONE': 0,
        'NO_CAPS': 10,
        'ALL_CAPS': 20,
        'SMALL_CAPS': 30,
        'TITLE_CASE': 40,
        'SENTENCE_CASE': 50,
        'PASCAL_CASE': 60,
        'CAMEL_CASE': 70,
        'SNAKE_CASE': 80,
        'KEBAB_CASE': 90
    }

    # Constants defining case values
    ALL_CAPS: int = _cases['ALL_CAPS']
    CAMEL_CASE: int = _cases['CAMEL_CASE']
    KEBAB_CASE: int = _cases['KEBAB_CASE']
    NONE: int = _cases['NONE']
    NO_CAPS: int = _cases['NO_CAPS']
    PASCAL_CASE: int = _cases['PASCAL_CASE']
    SENTENCE_CASE: int = _cases['SENTENCE_CASE']
    SMALL_CAPS: int = _cases['SMALL_CAPS']
    SNAKE_CASE: int = _cases['SNAKE_CASE']
    TITLE_CASE: int = _cases['TITLE_CASE']

    @classmethod
    def _all_caps(cls, message: str) -> str:
        """
        Converts the provided message to upper case.
        :param message: The message to be converted to uppercase.
        :type message: str
        :return: The converted message in upper case.
        :rtype: str
        """
        return message.upper()

    @classmethod
    def _camel_case(cls, message: str) -> str:
        """
        Converts the provided message to camel case.
        :param message: The message to be converted to camel case.
        :type message: str
        :return: The converted message in camel case.
        :rtype: str
        """
        cleaned_message = re.sub(r'[^a-zA-Z0-9_]+', ' ', message)
        return ''.join(
            word.capitalize() if i > 0 else word.lower()
            for i, word in enumerate(cleaned_message.split())
        )

    @classmethod
    def _kebab_case(cls, message: str) -> str:
        """
        Converts the provided message to kebab case.
        :param message: The message to be converted to kebab case.
        :type message: str
        :return: The converted message in kebab case.
        :rtype: str
        """
        cleaned_message = re.sub(r'[^a-zA-Z0-9]+', ' ', message)
        return '-'.join(word.lower() for word in cleaned_message.split())

    @classmethod
    def _no_caps(cls, message: str) -> str:
        """
        Converts the provided message to lower case.
        :param message: The message to be converted to lower case.
        :type message: str
        :return: The converted message in lower case.
        :rtype: str
        """
        return message.lower()

    @classmethod
    def _pascal_case(cls, message: str) -> str:
        """
        Converts the provided message to pascal case.
        :param message: The message to be converted to pascal case.
        :type message: str
        :return: The converted message in pascal case.
        :rtype: str
        """
        cleaned_message = re.sub(r'[^a-zA-Z0-9]+', ' ', message)
        return ''.join(word.capitalize() for word in cleaned_message.split())

    @classmethod
    def _sentence_case(cls, message: str) -> str:
        """
        Converts the provided message to sentence case.
        :param message: The message to be converted to sentence case.
        :type message: str
        :return: The converted message in sentence case.
        :rtype: str
        """
        return message.capitalize()

    @classmethod
    def _small_caps(cls, message: str) -> str:
        """
        Converts the provided message to small caps.
        :param message: The message to be converted to small caps.
        :type message: str
        :return: The converted message in small caps.
        :rtype: str
        """
        return ''.join(chr(ord(c.upper()) + 0xFEE0) if 'a' <= c <= 'z' else c for c in message)

    @classmethod
    def _snake_case(cls, message: str) -> str:
        """
        Converts the provided message to snake case.
        :param message: The message to be converted to snake case.
        :type message: str
        :return: The converted message in snake case.
        :rtype: str
        """
        cleaned_message = re.sub(r'[^a-zA-Z0-9]+', ' ', message)
        return '_'.join(word.lower() for word in cleaned_message.split())

    @classmethod
    def _title_case(cls, message: str) -> str:
        """
        Converts the provided message to title case.
        :param message: The message to be converted to title case.
        :type message: str
        :return: The converted message in title case.
        :rtype: str
        """
        return message.title()

    @classmethod
    def convert_text(cls, message: str, text_case: int) -> str:
        """
        Converts the provided message to the specified text case.
        :param message: The message to be converted.
        :type message: str
        :param text_case: The text case to which the message should be converted.
        :type text_case: str
        :return: The converted message.
        :rtype: str
        """
        Validate.validate_type(message, str, 'message should be a string.')
        Validate.validate_type(text_case, int, 'text_case should be an integer.')

        match text_case:
            case cls.ALL_CAPS:
                return cls._all_caps(message)
            case cls.CAMEL_CASE:
                return cls._camel_case(message)
            case cls.KEBAB_CASE:
                return cls._kebab_case(message)
            case cls.NONE:
                return message
            case cls.NO_CAPS:
                return cls._no_caps(message)
            case cls.PASCAL_CASE:
                return cls._pascal_case(message)
            case cls.SENTENCE_CASE:
                return cls._sentence_case(message)
            case cls.SMALL_CAPS:
                return cls._small_caps(message)
            case cls.SNAKE_CASE:
                return cls._snake_case(message)
            case cls.TITLE_CASE:
                return cls._title_case(message)
            case _:
                return message

    @classmethod
    def get_cases(cls) -> dict:
        """
        Generates a dictionary containing a list of all supported text cases.
        :return: The dictionary containing the list of supported text cases.
        :rtype: dict
        """
        return dict(sorted(cls._cases.items()))


class ColorMapper:
    """
    Offers functionality to create and manage mappings for text styles, including text color,
    background color, effects, and case transformations, based on keywords such as strings or
    regex patterns. These mappings are utilized with "echo" to style text within terminals.
    """

    def __init__(self) -> None:
        """
        Initializes the ColorMapper class.
        """
        self._mappings = {}

    def add_mapping(
            self,
            name: str,
            keywords: str | list[str],
            text_color: Optional[str] = None,
            text_background_color: Optional[str] = None,
            text_effect: Optional[str] = None,
            text_case: Optional[int] = TextCase.NONE,
            color_match: Optional[bool] = False,
            ignore_case: Optional[bool] = False
    ) -> None:
        """
        Allows the addition of a mapping to the dictionary for styling text based on specified keywords.
        :param name: The name for the mapping.
        :type name: str
        :param keywords: The list of keywords to match within the text and style if matching.
        This can include either a string or list of strings. Additionally, supports regex patterns.
        :type keywords: str | list[str]
        :param text_color: The ANSI color code to apply for text foreground color.
        :type text_color: str
        :param text_background_color: The ANSI color code to apply for text background color.
        :type text_background_color: str
        :param text_effect: The ANSI effect code to apply for text.
        :type text_effect: str
        :param text_case: The text case to apply to text.
        :type text_case: int
        :param color_match: Flag to colorize only the matching content of keyword.
        If True, colorize just the matching content, else the entire text will be colorized.
        :type color_match: bool
        :param ignore_case: Flag to ignore case while performing match. If True, ignores the case
        (case-insensitive) and matches the content, else case-sensitive match is performed.
        :type ignore_case: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(keywords, Union[str, list], 'keywords should either be a string or list of strings.')
        if isinstance(keywords, list):
            all(
                Validate.validate_type(keyword, str, 'keywords should either be a string or list of strings.')
                for keyword in keywords
            )
        Validate.validate_type(text_color, Union[str, None], 'text_color should be a string.')
        Validate.validate_type(text_background_color, Union[str, None], 'text_background_color should be a string.')
        Validate.validate_type(text_effect, Union[str, None], 'text_effect should be a string.')
        Validate.validate_type(text_case, Union[int, None], 'text_case should be an integer.')
        Validate.validate_type(color_match, Union[bool, None], 'color_match should be a boolean.')
        Validate.validate_type(ignore_case, Union[bool, None], 'ignore_case should be a boolean.')

        name = name.upper()
        if name in self._mappings:
            self._mappings[name]['keywords'] = [keywords] if isinstance(keywords, str) else keywords
            self._mappings[name]['color_mapping'] = {
                'text_color': text_color,
                'text_background_color': text_background_color,
                'text_effect': text_effect,
                'text_case': text_case
            }
            self._mappings[name]['flags'] = {
                'ignore_case': ignore_case,
                'color_match': color_match
            }
        else:
            self._mappings[name] = {
                'keywords': [keywords] if isinstance(keywords, str) else keywords,
                'color_mapping': {
                    'text_color': text_color,
                    'text_background_color': text_background_color,
                    'text_effect': text_effect,
                    'text_case': text_case
                },
                'flags': {
                    'ignore_case': ignore_case,
                    'color_match': color_match
                }
            }

    def get_mapping(self, name: str) -> dict:
        """
        Retrieves the mapping associated with the provided input name.
        :param name: The name of the mapping to be retrieved.
        :type name: str
        :return: The mapping in dictionary format corresponding to the provided input name.
        :rtype: dict
        """
        Validate.validate_type(name, str, 'name should be a string.')

        result = self._mappings.get(name.upper())
        if result is None:
            raise ValueError(f'"{name}" mapping not found.')

        return result

    def get_mappings(self) -> dict:
        """
        Generates a dictionary containing a list of all mappings.
        :return: The dictionary containing the list of mappings.
        :rtype: dict
        """
        return dict(sorted(self._mappings.items()))

    def is_valid_mapping(self, name: str) -> bool:
        """
        Checks whether the provided mapping name exists within the dictionary.
        :param name: The name of the mapping to be validated.
        :type name: str
        :return: True if the provided mapping exists, False otherwise.
        :rtype: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')

        try:
            return self.get_mapping(name) is not None
        except ValueError:
            return False

    def remove_mapping(self, name: str) -> None:
        """
        Deletes the mapping specified by name from the dictionary.
        :param name: The name of the mapping to be removed.
        :type name: str
        """
        Validate.validate_type(name, str, 'name should be a string.')

        if name.upper() in self._mappings:
            del self._mappings[name.upper()]


def _get_colorize_sequence(
        text_color: Optional[str] = None,
        text_background_color: Optional[str] = None,
        text_effect: Optional[str] = None
) -> str:
    """
    Produces a colorization sequence based on the provided inputs.
    :param text_color: The ANSI color code for the text foreground color.
    :type text_color: str
    :param text_background_color: The ANSI color code for the text background color.
    :type text_background_color: str
    :param text_effect: The ANSI effect code for the effect.
    :type text_effect: str
    :return: The generated colorized sequence.
    :rtype: str
    """
    colorize_sequence = (
        f'{text_color if text_color is not None else ""}'
        f'{text_background_color if text_background_color is not None else ""}'
        f'{text_effect if text_effect is not None else ""}'
    )
    return colorize_sequence


def get_colorized_message(
        message: str,
        text_color: Optional[str] = None,
        text_background_color: Optional[str] = None,
        text_effect: Optional[str] = None,
        text_case: Optional[int] = TextCase.NONE
) -> str:
    """
    Generates a colorized message based on the provided inputs.
    :param message: The message to be colorized.
    :type message: str
    :param text_color: The ANSI color code for the text foreground color.
    :type text_color: str
    :param text_background_color: The ANSI color code for the text background color.
    :type text_background_color: str
    :param text_effect: The ANSI effect code for the effect.
    :type text_effect:str
    :param text_case: The case to be applied for the text.
    :type text_case: str
    :return: The generated colorized message.
    :rtype: str
    """
    Validate.validate_type(message, str, 'message should be a string.')
    Validate.validate_type(text_color, Union[str, None], 'text_color should be a string.')
    Validate.validate_type(text_background_color, Union[str, None], 'text_background_color should be a string.')
    Validate.validate_type(text_effect, Union[str, None], 'text_effect should be a string.')
    Validate.validate_type(text_case, Union[int, None], 'text_case should be an integer.')

    if text_color is None and text_background_color is None and text_effect is None:
        return f'{TextCase.convert_text(message, text_case)}'

    colorize_sequence = _get_colorize_sequence(text_color, text_background_color, text_effect)
    return (
        f'{colorize_sequence}'
        f'{TextCase.convert_text(message, text_case)}'
        f'{RESET if colorize_sequence is not None else ""}'
    )


def get_colorized_message_by_regex_pattern(
        message: str,
        regex_pattern: str,
        text_color: Optional[str] = None,
        text_background_color: Optional[str] = None,
        text_effect: Optional[str] = None,
        text_case: Optional[int] = TextCase.NONE,
        color_match: Optional[bool] = False,
        ignore_case: Optional[bool] = False
) -> str:
    """
    Generates a colorized message based on the provided regex pattern and inputs.
    :param message: The message to be colorized.
    :type message: str
    :param regex_pattern: The regex pattern used to verify and colorize the matching text.
    :type regex_pattern: str
    :param text_color: The ANSI color code for the text foreground color.
    :type text_color: str
    :param text_background_color: The ANSI color code for the text background color.
    :type text_background_color: str
    :param text_effect: The ANSI effect code for the effect.
    :type text_effect: str
    :param text_case: The case to be applied for the text.
    :type text_case: str
    :param color_match: Flag to colorize only the matching content of keyword. If True,
    colorize just the matching content, else the entire text will be colorized.
    :type color_match: bool
    :param ignore_case: Flag to ignore case while performing match. If True, ignores the case
    (case-insensitive) and matches the content, else case-sensitive match is performed.
    :type ignore_case: bool
    :return: The generated colorized message.
    :rtype: str
    """
    Validate.validate_type(message, str, 'message should be a string.')
    Validate.validate_type(regex_pattern, str, 'regex_pattern should be a string.')
    Validate.validate_type(text_color, Union[str, None], 'text_color should be a string.')
    Validate.validate_type(text_background_color, Union[str, None], 'text_background_color should be a string.')
    Validate.validate_type(text_effect, Union[str, None], 'text_effect should be a string.')
    Validate.validate_type(text_case, Union[int, None], 'text_case should be an integer.')
    Validate.validate_type(color_match, Union[bool, None], 'color_match should be a boolean.')
    Validate.validate_type(ignore_case, Union[bool, None], 'ignore_case should be a boolean.')

    colorized_message = message
    colorize_sequence = _get_colorize_sequence(text_color, text_background_color, text_effect)

    if ignore_case:
        if color_match:
            colorized_message = re.sub(
                regex_pattern,
                lambda match: (
                    f'{colorize_sequence}'
                    f'{TextCase.convert_text(match.group(), text_case)}'
                    f'{RESET if colorize_sequence is not None else ""}'
                ),
                colorized_message,
                flags=re.IGNORECASE
            )
        else:
            if re.search(regex_pattern, colorized_message, re.IGNORECASE):
                colorized_message = (
                    f'{colorize_sequence}'
                    f'{TextCase.convert_text(colorized_message, text_case)}'
                    f'{RESET if colorize_sequence is not None else ""}'
                )
    else:
        if color_match:
            colorized_message = re.sub(
                regex_pattern,
                lambda match: (
                    f'{colorize_sequence}'
                    f'{TextCase.convert_text(match.group(), text_case)}'
                    f'{RESET if colorize_sequence is not None else ""}'
                ),
                colorized_message
            )
        else:
            if re.search(regex_pattern, colorized_message):
                colorized_message = (
                    f'{colorize_sequence}'
                    f'{TextCase.convert_text(colorized_message, text_case)}'
                    f'{RESET if colorize_sequence is not None else ""}'
                )

    return colorized_message


def get_colorized_message_by_mappings(
        message: str,
        mappings: ColorMapper
) -> str:
    """
    Generates a colorized message based on the provided mappings.
    :param message: The message to be colorized.
    :type message: str
    :param mappings: The mappings utilized for verifying and colorizing the matched text.
    :type mappings: ColorMapper
    :return: The generated colorized message.
    :rtype: str
    """
    Validate.validate_type(message, str, 'message should be a string.')
    Validate.validate_type(mappings, ColorMapper, 'mappings should be of ColorMapper type.')

    colorized_message = message
    for key, value in mappings.get_mappings().items():
        keywords = value.get('keywords', [])
        color_mappings = value.get('color_mapping', {})
        flags = value.get('flags', {})

        for keyword_pattern in keywords:
            if flags.get('ignore_case', False):
                if re.search(keyword_pattern, colorized_message, re.IGNORECASE):
                    text_color = color_mappings.get('text_color', '')
                    text_background_color = color_mappings.get('text_background_color', '')
                    text_effect = color_mappings.get('text_effect', '')
                    text_case = color_mappings.get('text_case', '')
                    colorize_sequence = _get_colorize_sequence(text_color, text_background_color, text_effect)
                    if flags.get('color_match', False):
                        colorized_message = re.sub(
                            keyword_pattern,
                            lambda match: (
                                f'{colorize_sequence}'
                                f'{TextCase.convert_text(match.group(), text_case)}'
                                f'{RESET}'
                            ),
                            colorized_message,
                            flags=re.IGNORECASE
                        )
                    else:
                        colorized_message = (
                            f'{colorize_sequence}'
                            f'{TextCase.convert_text(colorized_message, text_case)}'
                            f'{RESET}'
                        )

                    break
            else:
                if re.search(keyword_pattern, colorized_message):
                    text_color = color_mappings.get('text_color', '')
                    text_background_color = color_mappings.get('text_background_color', '')
                    text_effect = color_mappings.get('text_effect', '')
                    text_case = color_mappings.get('text_case', '')
                    colorize_sequence = _get_colorize_sequence(text_color, text_background_color, text_effect)
                    if flags.get('color_match', False):
                        colorized_message = re.sub(
                            keyword_pattern,
                            lambda match: (
                                f'{colorize_sequence}'
                                f'{TextCase.convert_text(match.group(), text_case)}'
                                f'{RESET}'
                            ),
                            colorized_message
                        )
                    else:
                        colorized_message = (
                            f'{colorize_sequence}'
                            f'{TextCase.convert_text(colorized_message, text_case)}'
                            f'{RESET}'
                        )

                    break

    return colorized_message


def echo(
        message: str,
        regex_pattern: Optional[str] = None,
        mappings: Optional[ColorMapper] = None,
        text_color: Optional[str] = None,
        text_background_color: Optional[str] = None,
        text_effect: Optional[str] = None,
        text_case: Optional[int] = TextCase.NONE,
        color_match: Optional[bool] = False,
        ignore_case: Optional[bool] = False
) -> None:
    """
    Prints text colorized within the terminal based on the provided inputs. Supports the following scenarios:
    1) Colorizing a message by specifying text foreground color, text background color, text effect, and text case.
    2) Colorizing a message by matching it with a regex pattern and specifying text foreground color, text
    background color, text effect, text case, ignore case, and color match.
    3) Colorizing a message by matching it with mappings (utilizing a ColorMapper) and specifying text foreground
    color, text background color, text effect, text case, ignore case, and color match.
    :param message: The message to be colorized.
    :type message: str
    :param regex_pattern: The regex pattern used to verify and colorize the matching text.
    :type regex_pattern: str
    :param mappings: The mappings utilized for verifying and colorizing the matched text.
    :type mappings: ColorMapper
    :param text_color: The ANSI color code for the text foreground color.
    :type text_color: str
    :param text_background_color: The ANSI color code for the text background color.
    :type text_background_color: str
    :param text_effect: The ANSI effect code for the effect.
    :type text_effect: str
    :param text_case: The case to be applied for the text.
    :type text_case: str
    :param color_match: Flag to colorize only the matching content of keyword. If True,
    colorize just the matching content, else the entire text will be colorized.
    :type color_match: bool
    :param ignore_case: Flag to ignore case while performing match. If True, ignores the case
    (case-insensitive) and matches the content, else case-sensitive match is performed.
    :type ignore_case: bool
    """
    if mappings is not None:
        Validate.validate_type(mappings, ColorMapper, 'mappings should be of ColorMapper type.')
    elif regex_pattern is not None:
        Validate.validate_type(regex_pattern, str, 'regex_pattern should be a string.')
        Validate.validate_type(color_match, bool, 'color_match should be a boolean.')
        Validate.validate_type(ignore_case, bool, 'ignore_case should be a boolean.')

    if mappings is None:
        Validate.validate_type(text_color, Union[str, None], 'text_color should be a string.')
        Validate.validate_type(text_background_color, Union[str, None], 'text_background_color should be a string.')
        Validate.validate_type(text_effect, Union[str, None], 'text_effect should be a string.')
        Validate.validate_type(text_case, Union[int, None], 'text_case should be an integer.')

    Validate.validate_type(message, str, 'message should be a string.')

    colorized_message = message

    if is_colorization_supported():
        if mappings is not None:
            colorized_message = get_colorized_message_by_mappings(colorized_message, mappings)
        elif regex_pattern is not None:
            colorized_message = get_colorized_message_by_regex_pattern(
                colorized_message, regex_pattern,
                text_color, text_background_color, text_effect, text_case,
                color_match, ignore_case
            )
        else:
            colorized_message = get_colorized_message(
                colorized_message, text_color, text_background_color, text_effect, text_case
            )

    print(colorized_message)
