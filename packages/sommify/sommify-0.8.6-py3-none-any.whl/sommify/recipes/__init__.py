import re
from unidecode import unidecode
from unicodedata import normalize
import html
from .. import utils
from .. import regex as patterns


def _format_attribute(attr):
    # replace spaces with underscores, and make lowercase
    return attr.lower().replace(" ", "_").replace("-", "_").replace("&", "and")


class Ingredient:
    def __init__(self, name, regex, parents, is_vague):
        parents = [p.lower() for p in parents]

        self.is_protein = "protein" in parents
        self.is_vegetable = "vegetables" in parents
        self.is_root_vegetable = "roots" in parents
        self.is_fruit = "fruits" in parents
        self.is_grain = "grains" in parents
        self.is_dairy = "dairy" in parents
        self.is_cheese = "cheese" in parents
        self.is_fat = "fat" in parents
        self.is_sweet = "sweeteners" in parents or "chocolate" in parents
        self.is_spice = "spices" in parents
        self.is_herb = "herbs" in parents
        self.is_liquid = "liquids" in parents or name == "milk"
        self.is_rhizome = "rhizomes" in parents
        self.is_cabbage = "cabbage" in parents

        self.name = name
        regex = patterns.one_of(regex)
        portion = rf"(?:{patterns.PORTION})"
        if self.is_protein:
            self.pattern = re.compile(rf"(?:{regex})(?: {portion})?$")
        elif self.is_cheese:
            portion = r"(?:slices?|cubes?|wedges?|rounds?|wheels?|cheese|rind|shavings?)"
            self.pattern = re.compile(rf"(?:{regex})(?: {portion})?$")
        elif self.is_rhizome:
            portion = r"(?:powder|rhizomes?|root|roots?|tubers?|tuber|tubers?)"
            self.pattern = re.compile(rf"(?:{regex})(?: {portion})?$")
        elif self.is_cabbage:
            portion = r"(?:leaf|leaves|heads?|florets?|stalks?)"
            self.pattern = re.compile(rf"(?:{regex})(?: {portion})?$")
        else:
            self.pattern = re.compile(rf"(?:{regex})$")

        self.parents = parents
        self.is_general = is_vague

    def __repr__(self):
        return f"Ingredient(name={self.name}, parents={self.parents}, is_general={self.is_general})"

    def __str__(self):
        return f"Ingredient(name={self.name}, parents={self.parents}, is_general={self.is_general})"


class IngredientFamily:
    def __init__(self, name="", vague=None, children=[]):
        self.name = name
        self.vague = vague

        for name, value in children:
            setattr(self, name, value)


    def __str__(self):
        return "\n".join([i.__str__() for i in self.get_ingredients()])

    def __repr__(self):
        return self.__str__()

    # when an index is accessed, return ingredient at that index
    def __getitem__(self, index):
        return self.get_ingredients()[index]

    # when an attribute is accessed, format it
    def __getattribute__(self, name):
        name = _format_attribute(name)
        return super().__getattribute__(name)

    # when an attribute is added to the class, format it
    def __setattr__(self, name, value):
        name = _format_attribute(name)
        super().__setattr__(name, value)

    # handle len
    def __len__(self):
        return len(self.get_ingredients())

    def get_ingredients(self):
        # recursively loop over subcategories, adding ingredients to list
        ingredients = self.ingredients.copy() if hasattr(self, "ingredients") else []
        for _, value in self.__dict__.items():
            if isinstance(value, IngredientFamily):
                ingredients.extend(value.get_ingredients())

        return ingredients

    def register_ingredient(self, name, regex, path=[]):
        is_vague = False
        if name.startswith("_"):
            name = name[1:]
            is_vague = True

        if len(path) == 0:
            if not hasattr(self, "ingredients"):
                self.ingredients = []
            self.ingredients.append(
                Ingredient(name=name, regex=regex, parents=path, is_vague=is_vague)
            )

        else:
            # loop over path keys, creating IngredientFamily objects as needed
            current = self
            for key in path:
                if not hasattr(current, key):
                    setattr(current, key, IngredientFamily(key))
                current = getattr(current, key)

            if not hasattr(current, "ingredients"):
                current.ingredients = []

            current.ingredients.append(
                Ingredient(name=name, regex=regex, parents=path, is_vague=is_vague)
            )

    def register_subcategory(self, name, vague, children):
        setattr(self, name, IngredientFamily(name, vague, children))

    def _normalize(self, phrase: str) -> str:
        phrase = normalize("NFD", phrase)
        phrase = unidecode(phrase)
        phrase = phrase.lower()
        phrase = re.sub(r"\([^)]*\)", "", phrase)
        phrase = re.sub(r"\(|\)", "", phrase)

        phrase = utils.P_vulgar_fractions(phrase)

        phrase = phrase.replace("–", "-")
        phrase = phrase.replace("⁄", "/")
        phrase = re.sub(r"half ?(?:and|-) ?half", "half-and-half", phrase)
        phrase = re.sub(r"\.\.+", "", phrase)
        phrase = re.sub(r" *\. *(?![0-9])", ". ", phrase)
        phrase = re.sub(r"(?<=[0-9]) *\. *(?=[0-9])", ".", phrase)
        phrase = re.sub(r" '", "'", phrase)
        phrase = re.sub(r"(,[^,]+)?< ?a href.*", "", phrase)
        phrase = re.sub(r""" *<(?:"[^"]*"['"]*|'[^']*'['"]*|[^'">])+> *""", "", phrase)
        phrase = re.sub(r"(?<=[a-z])/[a-z]+", "", phrase)
        phrase = re.sub(r"\b(?:5|five)[- ]?spice", "fivespice", phrase)
        phrase = re.sub(r".*: ?", "", phrase)
        phrase = re.sub(r"\s+", " ", phrase)
        phrase = re.sub(r"(?:1 )?& frac", "1 /", phrase)  # remove: 1 & frac
        phrase = re.sub(r"dipping sauce", "sauce", phrase)
        phrase = phrase.strip()
        return phrase

    def read_phrase(self, phrase: str) -> object:
        if not utils.P_filter(str(phrase)):
            return None

        phrase = html.unescape(phrase)
        phrase = self._normalize(phrase)
        phrase = utils.P_duplicates(phrase)
        phrase = utils.P_multi_misc_fix(phrase)
        phrase = utils.P_multi_adj_fix(phrase)
        phrase = utils.P_missing_multiplier_symbol_fix(phrase)
        phrase = utils.P_quantity_dash_unit_fix(phrase)
        phrase = utils.P_juice_zest_fix(phrase)
        phrase = utils.P_product_name_fix(phrase)
        phrase = utils.P_multi_color_fix(phrase)

        values = re.search(patterns.INGREDIENT, phrase).groupdict()

        values["unit"] = None
        if values["quantity"]:
            values["quantity"], values["unit"] = re.search(
                rf"(?P<quantity>{patterns.Q})? ?(?P<unit>.*)?", values["quantity"]
            ).groups()
            values["quantity"] = utils.Q_to_number(values["quantity"])

        values["unit"] = utils.U_unify(values["unit"])
        values["quantity"], values["unit"] = utils.Q_U_unify(
            values["quantity"], values["unit"]
        )

        values["size"] = utils.S_unify(values["size"])

        if values["ingredient"] != values["ingredient"] or not values["ingredient"]:
            return None

        values["ingredient"] = utils.I_to_singular(values["ingredient"])
        # values["simple"] = utils.I_label_protein(values["ingredient"])
        # values["simple"] = utils.I_simplify(values["simple"])

        # if utils.I_is_protein(values["ingredient"]):
        #     protein, portion = utils.I_protein_portion(values["ingredient"])
        #     values["ingredient"] = protein
        #     values["portion"] = portion

        # loop over ingredients, checking for a match
        best_match, best_range = None, 0
        for ingredient in self.get_ingredients():
            if ingredient.pattern.search(values["ingredient"]):
                match = ingredient.pattern.search(values["ingredient"])
                match_range = match.end() - match.start()
                if match_range > best_range:
                    best_match, best_range = ingredient, match_range

        return best_match



# create baseline IngredientFamily object
cookbook = IngredientFamily()



_nested_dictionary = {
    "FAT": {
        "oil": [r"oil", r"oil spray", r"cooking spray", r"canola", r"rapeseed"],
        "ghee": [r"ghee"],
        "butter": [r"butter margarine", r"margarine", r"butter", r"oleo"],
        "shortening": [r"shortening", r"crisco"],
        "fat": [r"suet", r"grease", r"drippings?", r"lard", r"fat"],
    },
    "EGG": {
        "egg": [
            r"(?<!chocolate )\beggs?",
            r"egg (?:beater )?substitute",
            r"egg wash",
        ],
        "egg yolk": [
            r"egg yolks?",
            r"yolks? of (?:the |an )?egg",
            r"yolks?",
        ],
        "egg white": [
            r"egg white",
            r"egg white substitute",
            r"whites? of (?:the |an )?egg",
            r"egg glair",
            r"albumen",
        ],
    },
    "HERBS": {
        "FLOWERS": {
            "lavender": [r"lavender(?: flower| petal)?"],
            "hibiscus": [r"hibiscus(?: flower| petal)?"],
            "rose": [r"rose(?: flower| petal)?"],
            "chamomile": [r"chamomile(?: flower| petal)?"],
            "_flower": [r"flower", r"blossom", r"petal"],
        },
        "LEAVES": {
            "tea": [r"tea", r"chai", r"tea powder"],
            "mint": [r"mint leaf", r"mint"],
            "shiso": [r"shiso"],
            "basil": [r"basil leaf", r"\bbasil"],
            "cilantro": [r"cilantro", r"coriander(?: cress)?"],
            "dill": [r"dill weed", r"dill"],
            "oregano": [r"oregano"],
            "thyme": [r"thyme leaf", r"thyme leave", r"thyme"],
            "parsley": [r"parsley", r"parsley leaf", r"parsley flake"],
            "rosemary": [r"rosemary leaf", r"rosemary"],
            "fenugreek": [
                r"fenugreek",
                r"fenugreek leaf",
                r"methi",
                r"methi leaf",
                r"greek clover",
                r"kasuri methi",
            ],
            "lovage": [r"lovage"],
            "sage": [r"\bsage leaf", r"\bsage", r"sage herb"],
            "epazote": [r"epazote(?: leaf| leaves| herbs?| sprigs?| stalks?)?"],
            "tarragon": [r"tarragon leaf", r"tarragon"],
            "chive": [r"\bchive", r"\bchive stalk"],
            "garlic chive": [r"garlic chives?", r"chinese chives?"],
            "bay leaf": [r"bay leaf", r"bay leaves?", r"bay"],
            "lemon balm": [r"lemon balm"],
            "lemongrass": [
                r"lemon ?grass",
                r"citronella",
                r"lemon verbena",
                r"lemon catnip",
            ],
            "marjoram": [r"marjoram"],
            "chervil": [r"chervil"],
            "savory": [r"savory", r"savory herb"],
            "watercress": [r"watercress(?: salad)?"],
            "sorrel": [r"sorrel"],
            "arugula": [r"arug[ua]la", r"roquette", r"rocket", r"rucola"],
            "curry": [r"curry leaf", r"curry leaves"],
            #
            "_herb": [r"herbs?", r"herb mix", r"herb blend", r"bouquet garni"],
        },
        "SPROUTS": {
            # "alfalfa": [r"alfalfa sprouts?"],
            # "bean sprout": [r"bean sprouts?"],
            # "lentil sprout": [r"lentil sprouts?"],
            # "mung bean sprout": [r"mung bean sprouts?"],
            # "radish sprout": [r"radish sprouts?"],
            # "sunflower sprout": [r"sunflower sprouts?"],
            "_sprout": [r"sprouts?", r"pea shoots?"],
        },
    },
    "FUNGI": {
        "MUSHROOMS": {
            "morel mushroom": [r"\bmorels?\b"],
            "cremini mushroom": [
                r"button mushrooms?",
                r"cremini(?: mushrooms?)?",
                r"baby port[oa]bell[oa]",
                r"chestnut.*mushrooms?",
                r"baby bella(?: mushrooms?)",
                r"brown.*mushroom",
                r"crimini(?: mushrooms?)?",
            ],
            "chanterelle": [
                r"chant[ea]?relle(?: mushrooms?)?",
                r"girolle(?: mushrooms?)?",
                r"golden.*mushroom",
            ],
            "black mushroom": [r"black.*mushroom"],
            "enoki mushroom": [r"enoki", r"beech", r"shimeji"],
            "oyster mushroom": [r"oyster", r"trumpet.*mushroom"],
            "shiitake mushroom": [
                r"shiitake",
                r"chinese.*mushroom",
                r"japanese.*mushroom",
            ],
            "porcini mushroom": [r"porcini", r"bolet", r"king mushroom"],
            "champignon mushroom": [
                r"field mushroom",
                r"port[ao]bell[ao]",
                r"straw mushroom",
                r"large mushroom",
                r"champignon",
            ],
            "_mushroom": [r"mushroom", r"mushroom cap", r"mushroom stem"],
        },
        "TRUFFLE": {
            "white truffle": [r"white truffle"],
            "black truffle": [r"black truffle", r"perigord truffle"],
            "winter truffle": [r"winter truffle"],
            "summer truffle": [r"summer truffle"],
            "burgundy truffle": [r"burgundy truffle"],
            "_truffle": [r"(?<!chocolate )truffle"],
        },
    },
    "PASTA": {
        "noodles": [r"noodles?", r"noodle nest", r"ramen"], 
        "pasta": [
            r"tricolore",
            r"fusillipasta",
            r"rigatoni",
            r"rotini",
            r"ziti",
            r"rigat[ie]",
            r"macaroni elbow",
            r"fusilli lunghi",
            r"pasta shell",
            r"pasta shapes?",
            r"vermicelli",
            r"gnocchi",
            r"manicotti(?: shells?)",
            r"spaghetti",
            r"penne",
            r"pappardelle",
            r"orecchiette",
            r"tagliatelle",
            r"macaroni",
            r"linguine",
            r"farfalle",
            r"fusilli",
            r"fettuccine",
            r"capellini",
            r"lasagn[ea]",
            r"angel hair",
            r"dital[io]ni",
            r"paccheri",
            r"tort[ei]glioni",
            r"cavatelli",
            r"conchiglie",
            r"orzo",
            r"risoni",
            r"ravioli",
            r"tortell[io]ni",
            r"\bpasta",
            r"spagg?hettini",
        ],
    },
    "GRAINS": {
        "rice": [
            r"\brice(?: grains?)?",
            r"\barborio(?: grains?)?",
            r"\bbasmati(?: grains?)?",
            r"\bbaldo(?: grains?)?",
            r"carnarolli(?: grains?)?",
            r"maratelli(?: grains?)?",
            r"vialone nano",
        ],
        "couscous": [r"cous[- ]?cous(?: grains?)?"],
        "buckwheat": [r"buckwheat(?: grains?)?"],
        "quinoa": [r"quinoa(?: grains?)?"],
        "millet": [r"millet(?: grains?)?"],
        "barley": [r"barley(?: grains?)?"],
        "oat": [r"oat(?: grains?)?", r"oatmeal(?: grains?)?"],
        "bulgur": [r"bulgh?[au]r (?:wheat|grains?|berry|berries)", r"bulgh?[au]r"],
        "farro": [r"farro(?: grains?)?"],
        "amaranth": [r"amaranth(?: grains?)?"],
        "teff": [r"teff(?: grains?)?"],
        "spelt": [r"spelt(?: grains?| berry| berries)?"],
        "sorghum": [r"sorghum(?: grains?)?"],
        "wheat": [r"wheat(?: grains?| berry| berries)?"],
        "rye": [r"rye(?: grains?| berry| berries)?"],
        "hominy": [r"hominy(?: grains?)?"],
        "germ": [r"germs?"],
        "_grain": [r"grains?"],
    },
    "FLOUR": {
        "wheat flour": [
            r"whole[ -]?(?:meal|wheat) flour",
            r"graham flour",
            r"teff flour",
            r"oat flour",
            r"buckwheat flour",
            r"quinoa flour",
            r"rye flour",
            r"spelt flour",
            r"sorghum flour",
            r"chickpea flour",
            r"gram flour",
            r"masa harina",
            r"amaranth flour",
            r"barley flour",
            r"rice flour",
            r"millet flour",
            r"corn ?flour",
            r"cornmeal",
            r"indian meal",
            r"potato flour",
            r"semolina flour",
            r"semolina",
            r"cream of wheat",
            r"farina",
            r"meal",
        ],
        "polenta": [r"polenta", r"grits?"],
        "bran": [r"bran", r"bran flake"],
        "_flour": [r"flour", r"all-purpose flour"],
    },
    "SAUCES & CONDIMENTS": {
        "salsa sauce": [r"salsa", r"rotel tomato chilies", r"^rotel"],
        "worcestershire sauce": [
            r"worcestershire(?: sauce)?",
            r"brown sauce",
            r"steak sauce",
            r"a\.?1\.?",
            r"hp sauce",
        ],
        "salsa verde": [r"salsa verde"],
        "hummus": [r"hummus"],
        "guacamole": [r"guacamole"],
        "barbecue sauce": [
            r"barbecue sauce",
            r"bbq sauce",
            r"diana original sauce",
        ],
        "teriyaki sauce": [r"teriyaki sauce"],
        "adobo sauce": [r"chipotle pepper adobo sauce"],
        "soy sauce": [
            r"shoyu",
            r"ketjap manis",
            r"soya? sauce",
            r"tamari",
            r"tamari sauce",
            r"tamari seasoning",
            r"maggi(?: liquid)?(?: sauce| seasoning)?",
            r"knorr(?: liquid)?(?: sauce| seasoning)?",
        ],
        "hoisin sauce": [r"hoisin.*sauce"],
        "tomato sauce": [
            r"pizza sauce",
            r"tomato sauce",
            r"tomato puree",
            r"passata(?: sauce)?",
            r"marinara(?: dipping)?(?: sauce)?",
        ],
        "fish sauce": [
            r"nam pla",
            r"fish sauce",
            r"shrimp sauce",
            r"anchovy sauce",
            r"oyster sauce",
            r"seafood sauce",
            r"nuoc mam",
            r"nuoc cham",
        ],
        "fish paste": [
            r"fish paste",
            r"shrimp paste",
            r"anchovy paste",
        ],
        "enchilada sauce": [r"enchilada sauce"],
        "cranberry sauce": [r"cranberry sauce", r"berry cranberry sauce"],
        "hot sauce": [
            r"pepper.*sauce",
            r"sriracha",
            r"adobo sauce",
            r"hot sauce",
            r"tabasco(?: sauce)?",
            r"chill?[ei] sauce",
            r"buffalo sauce",
            r"habanero sauce",
        ],
        "garlic sauce": [r"garlic sauce"],
        "chili paste": [
            r"chill?i?[iey].*paste",
            r"adobo.*(?:paste|sauce)",
            r"ranchero.*sauce",
            r"sambal oelek",
            r"harissa",
            r"harissa paste",
            r"pepper paste",
            r"chipotle paste",
        ],
        "cheese sauce": [r"cheese sauce", r"alfredo sauce"],
        "curry paste": [r"curry.*paste"],
        "bean paste": [r"bean paste"],
        "tomato paste": [r"tomato.*(paste|concentrate)"],
        "grain mustard": [r"grainy? mustard"],
        "dijon mustard": [r"dijon mustard", r"dijon"],
        "mustard": [r"mustard"],
        "mayonnaise": [r"miracle whip", r"mayo", r"mayonnaise"],
        "pesto": [r"pesto"],
        "tahihi": [
            r"tahin[ai](?: sauce| paste| dressing)?",
            r"sesame (paste|dressing|sauce)",
        ],
        "ketchup": [r"ketchup", r"catsup", r"cetchup"],
        "_sauce": [r"sauce", r"dip"],
    },
    "SPICES": {
        "PEPPERCORN": {
            "white pepper": [r"(?:whole )?white (?:ground |whole )?pepper(?:corns?)?"],
            "pink pepper": [r"(?:whole )?pink (?:ground |whole )?pepper(?:corns?)?"],
            "sichuan pepper": [
                r"(?:whole )?sz?[ei]ch[uw]an (?:ground |whole )?pepper(?:corns?)?",
                r"pimi?ento berr(?:ies|y)",
                r"sansho pepper",
                r"japanese pepper",
                r"cubeb pepper",
                r"australian mountain pepper",
            ],
            "green peppercorn": [
                r"(?:whole )?green (?:ground |whole )?peppercorns?",
            ],
            "black pepper": [
                r"(?:whole )?black (?:ground |whole )?pepper(?:corns?)?",
                r"^pepper(?:corns?)?",
                r"pepper powder",
                r"ground pepper(?:corns?)?",
                r"black pepper(?:corns?)?",
                r"^pepper(?:corns?)?",
                r"grains of paradise",
            ],
        },
        "SEASONINGS": {
            "italian seasoning": [
                r"italian spices?(?: mix| blend)?",
                r"italian herbs?",
                r"italian.*seasoning(?: mix| blend)?",
            ],
            "greek seasoning": [
                r"greek.*seasoning(?: mix| blend)?",
                r"greek.*spices?(?: mix| blend)?",
            ],
            "herbes de provence": [
                r"herbes? de provence(?: seasoning| seasoning mix| seasoning blend| mix| blend)?",
            ],
            "sazon goya": [r"sazon goya"],
            "za'atar seasoning": [r"za'?atar(?: seasoning| seasoning mix| seasoning blend| mix| blend| spice mix| spice)?"],
            "jerk seasoning": [r"jerk spice", r"jerk seasoning"],
            "_seasoning": [r"seasoning", r"seasoning mix", r"seasoning blend"],
        },
        "BAKING SPICES": {
            "cinnamon": [r"(cinn?amm?on|cassia)(?: stick| bark| powder)?"],
            "nutmeg": [r"nutmeg"],
            "allspice": [r"all ?spice(?: berry| berries)?"],
            "clove": [r"cloves?"],
            "mace": [r"mace"],
            "anise": [r"anise(?: essence| extract| powder)", r"aniseed(?: powder)?", r"anise seed(?: powder)?"],
            "vanilla": [
                r"vanilla essence",
                r"^vanilla",
                r"vanilla extract",
                r"vanilla pod",
                r"vanilla bean",
                r"vanilla bean paste",
                r"vanilla paste",
            ],
            "cardamom": [
                r"cardamom powder",
                r"cardamom",
                r"cardamom pods?",
                r"cardamom seeds?",
            ],
            "almond extract": [
                r"almond extract",
                r"almond essence",
                r"almond oil",
                r"almond flavoring",
                r"almond paste"
            ],
            "_baking spice": [r"baking spices?"],
        },
        "OTHER SPICES": {
            "msg": [
                r"accent seasoning",
                r"msg",
                r"monosodium glutamate",
                r"glutamate",
            ],
            "masala": [r"masala(?: powder| mix| blend| seasoning)?"],
            "ras el hanout": [
                r"moroccan spice",
                r"ras? el hanout(?: spice)?(?: mix)?",
            ],
            "sumaq": [r"suma[cq]"],
            "paprika": [r"paprika"],
            "onion powder": [
                r"onion granules?",
                r"onion powder",
                r"onion flakes?",
            ],
            "garlic powder": [
                r"garlic granules?",
                r"garlic flakes?",
                r"garlic powder",
            ],
            "salt": [
                r"\bsalt(?:.*pepper)?",
                r"\bsalt",
                r"sea-salt",
                r"salt flakes?",
                r"salt substitute",
                r"fleur de sel",
                r"salt;",
            ],
            "mustard powder": [r"mustard powder"],
            "coriander powder": [r"coriander powder"],
            "fivespice": [r"fivespice(?: powder| blend)?"],
            "spicy powder": [
                r"cayenne(?: pepper)?",
                r"chill?[iey] powder",
                r"(?:chipotle|habanero|poblano|pepperoncino|cayenne).*powder",
                r"chill?[eiy] flakes?",
                r"pepper flakes?",
            ],
            "saffron": [r"saffron(?: threads?| strands?| powder)?"],
            "curry powder": [r"curry.*powder", r"curry"],
            "amchur": [r"amchur", r"mango powder", r"amchoor"],
            "asafoetida": [r"asafoetida", r"hing", r"asafoetida powder"],
            "lemon pepper": [r"lemon[- ]?pepper"],
            "_spice": [r"\bspices?"],
        },
    },
    "NUTS": {
        "cashew": [r"\bcashew(?: nuts?)?"],
        "chestnut": [r"(?<!water )chest ?nuts?"],
        "walnut": [r"walnut(?: hal(?:f|ves))?"],
        "peanut": [r"peanut", r"groundnuts?"],
        "almond": [r"almond", r"macadamia(?: nuts?)?"],
        "pistachio": [r"pistachio(?: nuts?)?", r"pistachios"],
        "pecan": [r"pecan(?: nuts?)?"],
        "hazelnut": [r"hazel ?nut"],
        "pine nut": [r"pine ?nut"],
        "_nut": [r"\bnut", r"sacha inchi", r"acorns?", r"butternuts?"],
    },
    "SEEDS": {
        "chia": [r"chia(?: seed)?"],
        "anise": [r"anise(?: seed)?"],
        "mustard seed": [r"mustard seed"],
        "sesame": [r"sesame seeds?", r"sesame"],
        "poppy": [r"poppy seeds?", r"poppy"],
        "sunflower seed": [r"sunflower seed", r"sunflower"],
        "flaxseed": [r"flaxseed", r"linseed"],
        "ajwain": [r"ajwain", r"ajwain seeds?", r"lovage seeds?"],
        "pumpkin seed": [r"pumpkin seed", r"pepitas?"],
        "cumin": [
            r"cumin(?: powder)?",
            r"jeera(?: powder)?",
            r"nigella seed",
            r"caraway(?: seed)?",
        ],
        "_seed": [r"\bseed"],
    },
    "VEGETABLES": {
        "OTHER": {
            "eggplant": [
                r"eggplants?",
                r"aubergines?",
                r"brinjal",
                r"guinea squash",
            ],
            "asparagus": [r"asparagus spears?", r"asparagus tips?", r"asparagus"],
            "samphire": [r"samphire"],  # similar to asparagus
            "cucumber": [r"cucumbers?"],
            "tomato": [r"tomato(?:es)?"],
            "tomatillo": [r"tomatillos?", r"husk tomato(?:es|s)?"],
            "artichoke": [r"(?<!jerusalem )artichokes?(?: hearts?)?"],
            "corn": [
                r"\bmaize",
                r"ear corn",
                r"mexican corn",
                r"sweetcorn",
                r"mexicorn",
                r"corn cob",
                r"white corn",
                r"kernel",
                r"corn niblet",
                r"corn",
                r"shoepeg corn",
            ],
            "hot pepper": [
                r"roquito(?: pepper)?",
                r"chipotle chile",
                r"chill?[iey](?: pepper)?",
                r"hot pepper",
                r"jalapeno(?: pepper)?",
                r"serrano(?: pepper)?",
                r"poblano(?: pepper)?",
                r"scotch bonnet(?: pepper)?",
                r"habanero(?: pepper)?",
                r"peppadew(?: pepper)?",
                r"chipotle(?: pepper)?",
                r"pepperoncin[io](?: pepper)?",
                r"italian pepper",
                r"espelette pepper",
                r"banana pepper",
                r"anaheim chili",
                r"pimi?ento(?: pepper)?",
                r"\bchile",
                r"\bchilly",
                r"\bchilis?",
                r"cherry pepper",
                r"romano pepper",
                r"padron pepper",
                r"new mexico pepper",
                r"aji amarillo pepper",
                r"lime pepper",
                r"thai pepper",
                r"ancho pepper",
                r"ancho chill?[eiy]",
                r"[^^]pepper",
            ],
            "bell pepper": [
                r"piquillo peppers?",
                r"green peppers?",
                r"yellow pepperw?",
                r"capsicum",
                r"bell peppers?",
                r"sweet peppers?",
                r"cubanelle peppers?",
                r"red peppers?",
                r"orange peppers?"
            ],
            "okra": [
                r"okra", 
                # r"ladyfinger" # this needs to be solved in the future
            ],
        },
        "SQUASH": {
            "pumpkin": [r"pumpkin", r"jack-o-lantern", r"jack o lantern"],
            "zucchini": [r"zucchinis?", r"courgettes?"],
            "pattypan squash": [r"pattypan squash", r"pattypan"],
            "acorn squash": [r"acorn squash", r"acorn pumpkin", r"pepper squash"],
            "butternut squash": [r"butternut squash", r"butternut pumpkin"],
            "_squash": [r"squash", r"summer squash", r"winter squash"],
        },
        "LEGUMES": {
            "sprout": [r"\bsprouts?"],
            "lentil": [r"\blentil(?:s?| bean)"],
            "pea": [r"^snow", r"\bpea(?:s?| bean)", r"petit pois", r"mangetout"],
            "dal": [
                r"\bchann?a\b",
                r"\bur[ai]d\b",
                r"\btoor\b",
                r"\bdhal",
                r"\bdal",
                r"\bpulse",
            ],
            "edamame": [r"\bsoy beans?", r"\bedamame(?:s?| bean)"],
            "chickpea": [r"\bchickpeas?", r"\bbengal\b", r"\bgarbanzo\b"],
            "bean": [
                r"\brajma\b",
                r"\bbeans?",
                r"bean kidney",
                r"\bcannellini(?:s?| bean)",
            ],
        },
        "ROOTS": {
            "OTHER": {
                "wasabi": [r"wasabi(?: paste|\*| powder)?"],
                "horseradish": [r"horseradish"],
                "radish": [r"radish(?:es)?"],
                "burdock": [r"burdock"],
                "carrot": [r"carrot"],
                "daikon": [r"daikon", r"daikon radish(?:es)?"],
                "parsnip": [r"parsnip"],
                "turnip": [r"turnip", r"swede", r"rutabaga"],
                "beet": [r"beet", r"beetroot"],
                "celery": [r"celery(?: sticks?| roots?| hearts?| ribs?)?", r"celeriac"],
                "fennel": [r"fennel(?: bulb| root)?"],
            },
            "TUBERS": {
                "sunchoke": [r"sunchoke", r"jerusalem artichoke"],
                "bamboo shoot": [r"bamboo shoot", r"bamboo"],
                "oca": [r"oca"],
                "potato": [
                    r"potato",
                    r"spud",
                    r"french fry",
                    r"tater",
                    r"tater tots?",
                    r"potato flakes?",
                    r"hash brown",
                ],
            },
            "TUBEROUS": {
                "jicama": [r"jicama", r"yam bean"],
                "cassava": [r"cassava", r"yucc?a"],
                "sweet potato": [r"sweet potato", r"kumara", r"batata"],
                "yam": [r"yam"],
                "yacon": [r"yacon"],
                "ube": [r"ube"],
            },
            "CORMS": {
                "taro": [r"taro", r"dasheen"],
                "eddoe": [r"eddoe"],
                "water chestnut": [r"water chestnut"],
                "konjac": [r"konjac"],
            },
            "RHIZOMES": {
                "ginger": [
                    r"ginger ?(?:root|paste|powder)",
                    r"root ginger",
                    r"ginger",
                ],
                "gingseng": [r"gingse?ng"],
                "turmeric": [r"turmeric"],
                "galangal": [r"galangal"],
                "arrowroot": [r"arrowroot"],
            },
            "BULBS": {
                "leek": [r"leeks?", r"leek stalks?"],
                "scallion": [
                    r"green onions?",
                    r"spring onions?",
                    r"scallions?",
                    r"onion tops?",
                    r"scallion tops?",
                ],
                "pearl onion": [
                    r"pearl onions?",
                    r"baby onions?",
                    r"pickling onions?",
                    r"cocktail onions?",
                ],
                "garlic": [
                    r"garlics?",
                    r"garlic cloves?",
                    r"garlic bulbs?",
                    r"garlic heads?",
                    r"garlic paste",
                ],
                "shallot": [r"shallots?", r"eschal?lots?"],
                "onion": [r"\bonions?", r"onion rings?"],
            },
            #
            "_root vegetable": [
                r"root vegetables?",
                r"root veggies?",
                r"root veg",
            ],
        },
        "LEAVES": {
            "BEET": {
                "chard": [r"(?:swiss )?chard"],
                "spinach": [r"spinach(?: lea(?:f|ves))?"],
                #
                "_beet greens": [r"beet ?greens?"],
            },
            "LETTUCE": {
                "romaine lettuce": [
                    r"romaine(?: lettuce| lettuce heart)?",
                    r"cos(?: lettuce)?",
                    r"co lettuce",
                ],
                "iceberg lettuce": [r"iceberg(?: lettuce)?", r"crisphead(?: lettuce)?"],
                "butter lettuce": [
                    r"butter lettuce",
                    r"boston lettuce",
                    r"bibb(?: lettuce)?",
                ],
                #
                "_lettuce": [
                    r"(?:head |heart |leaf |leaves )?lettuce",
                    r"lettuce(?: head| heart| leaf| leaves)?",
                ],
            },
            "CHICORY": {
                "ENDIVE": {
                    "escarole": [r"escaroles?"],
                    "puntarelle": [r"puntarelles?"],
                    "belgian endive": [r"belgian endives?", r"witloofs?"],
                    "_endive": [r"endives?", r"frisee"],
                },
                "OTHER": {
                    "radicchio": [r"radicchio"],
                },
                "_chicory": [r"chicory"],
            },
            "CABBAGE": {
                "broccoli": [
                    r"broccoli",
                    r"broccolini",
                    r"broccoli (rabe|florets?)",
                ],
                "cauliflower": [r"cauliflower"],
                "romanesco": [r"romanesco", r"romanesco broccoli"],
                "red cabbage": [r"red cabbage", r"purple cabbage", r"january king"],
                "savoy cabbage": [r"savoy cabbage"],
                "napa cabbage": [
                    r"napp?a(?: cabbage| leaf)?",
                    r"chinese(?: cabbage| leaf)",
                    r"wombok(?: cabbage| leaf)?",
                ],
                "bok choy": [r"bok cho[iy]", r"pak cho[yi]"],
                "kale": [r"\bkale", r"cavolo nero"],
                "collard": [r"collard greens?", r"collards?"],
                "brussels sprout": [r"brussels? sprouts?"],
                #
                "kimchi": [r"kimchi"],
                "sauerkraut": [r"sauer ?kraut"],
                "_cabbage": [r"cabbage", r"kraut"],
            },
            #
            "_greens": [r"greens?", r"salad"],
        },
        #
        "_vegetable": [r"vegetables?", r"veg", r"^veggies?"],
    },
    "FRUITS": {
        "SAVORY": {
            "avocado": [r"avocado(?: pears?)?", r"alligator pears?"],
            "olive": [r"olives?", r"olive fruit"],
            "caper": [r"capers?", r"caper berr(?:y|ies)"],
        },
        "BERRY": {
            "blueberry": [r"blueberr(?:ies|y)?"],
            "strawberry": [r"straberr(?:ies|y)?"],
            "raspberry": [r"raspberr(?:ies|y)?"],
            "blackberry": [r"blackberr(?:ies|y)?"],
            "gooseberry": [r"gooseberr(?:ies|y)?"],
            "elderberry": [r"elderberr(?:ies|y)?"],
            "cranberry": [r"cranberr(?:ies|y)?"],
            "lingonberry": [r"lingon ?berr(?:ies|y)?"],
            "huckleberry": [r"huckleberr(?:ies|y)?"],
            "currant": [r"redcurrant", r"currant", r"currant ?berr(?:y|ies)"],
            #
            "_berry": [r"berr(?:ies|y)?", r"olallieberry", r"cloudberry"],
        },
        "MELONS": {
            "cantaloupe": [r"cantaloupe", r"muskmelon", r"rockmelon"],
            "honeydew melon": [r"honeydew", r"honeydew melon"],
            "watermelon": [r"watermelon"],
            #
            "_melon": [r"melon"],
        },
        "TROPICAL": {
            "guava": [r"guava"],
            "banana": [r"bananas?", r"plantains?"],
            "lychee": [r"lychee", r"litchi"],
            "kiwi": [r"kiwi fruit", r"kiwi", r"chineese gooseberry"],
            "mango": [r"mango(?:es)?"],
            "papaya": [r"papayas?"],
            "passion fruit": [r"passion ?fruits?"],
            "pineapple": [
                r"pineapple rings?",
                r"pineapple",
                r"pineapple tidbits?",
                r"pineapple chunks?",
                r"ananas",
            ],
            "coconut": [
                r"coconut",
                r"coconut meat",
                r"coconut flakes?",
                #
                r"cream of coconut",
                r"coconut extract",
                r"cream coconut",
            ],
            "heart of palm": [
                r"hearts? of palm",
                r"palm hearts?",
                r"palm cores?",
                r"palmito",
                r"chonta",
            ],
            "dragonfruit": [r"dragonfruit", r"pitaya"],
            "starfruit": [r"starfruit", r"carambola"],
            "tamarind": [r"tamarindo?( pulp| paste)?"],
            #
            "_tropical fruit": [r"tropical fruits?"],
        },
        "APPLES & PEARS": {
            "apple": [r"apples?", r"apple ?sauce"],
            "pear": [r"pears?"],
            "quince": [r"quinces?"],
        },
        "CITRUS": {
            "lemon": [r"lemon", r"citron"],
            "lime": [r"lime"],
            "tangerine": [r"tangerine", r"clementine", r"mandarine?(?: orange)?"],
            "orange": [r"orange", r"orange sections?"],
            "grapefruit": [r"grapefruit"],
            "kumquat": [r"kumquat"],
            #
            "_citrus": [r"citrus", r"citrus fruit"],
            "ZEST": {
                "lime zest": [r"lime(?:'s)? (zest|rind|peel)"],
                "orange zest": [r"orange(?:'s)? (zest|rind|peel)"],
                "grapefruit zest": [r"grapefruit(?:'s)? (zest|rind|peel)"],
                "tangerine zest": [r"tangerine(?:'s)? (zest|rind|peel)"],
                "lemon zest": [r"lemon(?:'s)? (zest|rind|peel)", r"zest"],
            },
            "JUICE": {
                "lemon juice": [
                    r"lemon juice",
                    r"lemonade concentrate",
                    r"lemon extract",
                ],
                "lime juice": [r"lime juice", r"limeade", r"limeade concentrate"],
                "orange juice": [
                    r"orange juice",
                    r"orange juice concentrate",
                    r"oj",
                    r"orange extract",
                ],
                "grapefruit juice": [r"grapefruit juice"],
            },
        },
        "OTHER": {
            "date": [r"dates?"],
            "fig": [r"figs?"],
            "grape": [r"grapes?"],
            "plum": [r"plums?", r"prunes?"],
            "pomegranate": [r"pomegranates?"],
            "cherry": [r"cherr(?:ies|y)"],
            "rhubarb": [r"rhubarb"],
            "peach": [r"peach(?:es)?", r"nectarines?"],
            "apricot": [r"apricots?"],
            "persimmon": [r"persimmons?", r"kaki"],
        },
        #
        "_fruit": [r"fruits?", r"fruit salad"],
    },
    "DAIRY": {
        "CREAM": {
            "light cream": [
                r"light cream",
                r"nonfat cream",
                r"half cream",
                r"single cream",
                r"half and half",
                r"half-and-half",
                r"table cream",
                r"coffee cream",
                r"creamer",
            ],
            "whipped cream": [r"cool whip", r"whipped cream"],
            "sour cream": [
                r"creme fraiche",
                r"sour(?:ed)? cream",
                r"schmand",
                r"mexican cream",
                r"mexican crema"
            ],
            "clotted cream": [r"clotted cream", r"devonshire cream"],
            "ice cream": [r"ice cream"],
            "heavy cream": [
                r"double cream",
                r"whipping cream",
                r"thick cream",
                r"cream",
                r"3[0-8] ?% ?cream",
            ],
        },
        "CHEESE": {
            "parmesan": [
                r"parmesan cheese",
                r"parmesan",
                r"grana? padano",
                r"parmigiano",
                r"parmigiano regg?iano",
                r"regg?iano",
            ],
            "pecorino": [r"pecorino", r"romano"],
            "mozzarella": [
                r"mozzarella cheese",
                r"mozzarella",
                r"stracciatella",
                r"stracciatella cheese",
                r"fior ?di ?latte",
                r"burrata",
                r"bocconcini",
            ],
            "ricotta": [r"ricotta"],
            "mascarpone": [r"mascarpone"],
            "cottage cheese": [
                r"cottage cheese",
                r"cottage",
                r"farmers? cheese",
                r"pot cheese",
                r"curd cheese",
                r"curd",
                r"quark",
            ],
            "monterey jack": [
                r"monterey jack(?: cheese)?(?: blend)?",
                r"pepper ?jack(?: cheese)?(?: blend)?",
            ],
            "mexican cheese": [
                r"queso fresco",
                r"mexican cheese(?: blend)?",
                r"asadero",
                r"panela",
            ],
            "feta": [r"\bfeta"],
            "gruyere": [r"gruyere(?: cheese)?"],
            "swiss cheese": [r"swiss cheese", r"emmenth?al(?:er)?"],
            "cream cheese": [r"cream cheese", r"neufchatel", r"fromage frais"],
            "cheddar": [
                r"cheddar cheese",
                r"cheddar(?: cheese(?: blend| round| mix)?)?",
                r"caerphilly(?: cheese(?: blend| round| mix)?)?",
            ],
            "brie": [
                r"brie(?: cheese)?",
                r"camembert(?: cheese)?",
            ],
            "paneer": [r"pan(?:ee|i)r(?: cheese)?"],
            "halloumi": [
                r"halloumi(?: cheese)?",
                r"hellim(?: cheese)?",
                r"hallumi(?: cheese)?",
                r"cypriot cheese",
            ],
            "blue cheese": [
                r"blue(?: cheese)?",
                r"blue cheese crumble",
                r"gorgonzola(?: cheese)?",
                r"roquefort(?: cheese)?",
                r"stilton(?: cheese)?",
                r"danish blue(?: cheese)?",
                r"bleu(?: cheese)?",
            ],
            "goat cheese": [
                r"goat'?s? cheese(?: blend| round| mix)?",
                r"chevre",
                r"chevre cheese",
                r"chevre log",
                r"chevre roll",
            ],
            #
            "_cheese": [
                r"fontina",
                r"gouda",
                r"cheese(?: (?:blend|rolls?|mix|rounds?|wedges?|slices?|food))?",
                r"provolone",
                r"asiago",
                r"ei?dam",
                r"colby",
            ],
        },
        "MILK & YOGHURT": {
            "milk": [r"\bmilk", r"soymilk"],
            "yoghurt": [
                r"sour(?:ed)? milk",
                r"buttermilk",
                r"yogh?o?urt",
                r"yoghurt",
                r"kefir",
                r"cultured milk",
            ],
            "milk powder": [
                r"milk powder",
                r"powdered milk",
                r"dried milk",
                r"dehydrated milk",
            ],
        },
    },
    "BAKING": {
        "OTHER": {
            "nut butter": [r"(?:nut|cashew|almond).*butter"],
            "nutella": [r"nutella"],
            "caramel": [
                r"caramel",
                r"toffee",
                r"dulce de leche",
                r"caramel sauce",
                r"caramel topping",
            ],
            "custard": [r"custard", r"creme anglaise", r"custard powder"],
            "icing": [r"icing", r"frosting"],
            "sprinkle": [r"sprinkle"],
            "marzipan": [r"marzipan(?: chunks?)?"],
            "baking powder": [r"baking powder", r"baking powder mix"],
            "baking soda": [
                r"baking soda",
                r"sodium bicarbonate",
                r"bicarbonate of soda",
            ],
            "cream of tartar": [r"cream tartar", r"cream of tartar", r"potassium bitartrate"],
            "maraschino cherry": [r"glace cherry"],
            "english pudding": [r"english pudding", r"christmas pudding"],
            "yorkshire pudding": [r"yorkshire pudding"],
            "pudding": [r"pudding", r"pudding mix"],
            "baking mix": [
                r"baking (mix|dough)",
                r"bread (mix|dough)",
                r"cornbread (mix|dough)",
                r"pancake (mix|dough)",
                r"biscuit (mix|dough)",
                r"muffin (mix|dough)",
                r"cake (mix|dough)",
                r"bisquick",
            ],
            "pizza dough": [r"pizza dough", r"pizza base", r"pizza crust"],
            "pie crust": [
                r"pie dough",
                r"pie shell",
                r"crust pie",
                r"pie crust",
                r"pastry shell",
                r"pastry dough",
                r"pastry",
                r"pastry crust",
                r"cracker crust",
                r"cracker crumb",
                r"shortcrust pastry",
            ],
            "wafer": [r"wafers?"],
            "sponge cake": [r"sponge cake", r"genoise", r"angel food cake"],
            "cake": [r"pound cake", r"madeira cake", r"cake"],
            "food coloring": [r"colou?ring", r"colou?ring paste"],
            "rice paper": [r"rice paper", r"spring roll wrapper", r"spring wrapper", r"egg roll wrap"],
            "wonton wrapper": [r"wonton wrapper"],
            "puff pastry": [r"puff pastry"],
            "phyllo pastry": [r"(phyllo|filo)(?: pastry| dough)?"],
        },
        "BREADS & ROLLS": {
            "pretzel": [r"pretzel", r"pretzel roll"],
            "roll": [
                r"roll",
                r"bun",
                r"^french",
                r"^crescent",
                r"^kaiser",
                r"hoagie",
                r"crescent dinner",
                r"french baguette",
                r"baguette",
                r"brioche",
                r"croissants?",
                r"challah",
            ],
            "toast": [r"toast", r"toast bread"],
            "bread": [r"bread", r"ciabatta", r"english muffin", r"sourdough"],
            "cookie": [r"cookies?", r"gingersnap", r"oreos?"],
            "ladyfinger": [
                r"ladyfingers?",
                r"ladyfinger biscuits?",
                r"savoiardi",
                r"sponge fingers?",
                r"sponge biscuits?",
            ],
            "biscuit": [r"biscuits?"],
            "cracker": [r"cracker", r"matzo"],
            "tortilla": [r"tortilla", r"egg wraps?", r"tostadas?", r"taco shells?"],
            "pita bread": [r"pita breads?", r"pitas?", r"pita pockets?"],
        },
        "SWEETENERS": {
            "sugar": [
                r"sugar substitute",
                r"sugar blend",
                r"jaggery",
                r"sweetener",
                r"splenda",
                r"splenda blend",
                r"splenda granular",
                r"sugar",
            ],
            "glucose": [r"glucose", r"glucose syrup"],
            "stevia": [r"stevia"],
            "molasses": [r"molasses", r"molass", r"treacle"],
            "syrup": [r"syrup", r"agave nectar", r"sirup"],
            "honey": [r"honey", r"miele"],
        },
        "CHOCOLATE": {
            "cocoa": [r"(?:cacao|cocoa)(?: nib| powder)?"],
            "coffee": [
                r"black cofee",
                r"espresso",
                r"coffee",
                r"espresso powder",
                r"coffee granule",
                r"coffee powder",
                r"\bcoffee beans?\b",
                r"espresso bean",
            ],
            "dark chocolate": [
                r"dark chocolate",
                r"bittersweet chocolate",
                r"semisweet chocolate",
            ],
            "white chocolate": [r"white chocolate", r"white baking chocolate"],
            "chocolate": [
                r"chocolate shavings?",
                r"chocolate bars?",
                r"chocolate baking squares?",
                r"chocolate",
                r"chocolate squares?",
                r"chocolate chips?",
                r"chocolate morsels?",
                r"chocolate curls?",
                r"chocolate sauce",
                r"chocolate buttons?",
            ],
        },
    },
    "LIQUIDS": {
        "COCKTAILS": {
            "sweet sour mix": [r"^mix", r"sour mix"],
            "grenadine": [r"grenadine"],
        },
        "OTHER": {
            "flower water": [r"flower ?water", r"rose ?water", r"blossom ?water"],
            "sparkling water": [
                r"sparkling water",
                r"carbonated water",
                r"seltzer water",
                r"club soda",
                r"soda water",
                r"mineral water",
                r"tonic water",
            ],
            "sugary soda": [
                r"soda pop",
                r"soda",
                r"pop",
                r"cola",
                r"sprite",
                r"fanta",
                r"pepsi",
                r"coke",
                r"lemonade",
            ],
            "_water": [
                r"water",
            ],
        },
        "STOCKS & SOUPS": {
            "chicken stock": [
                r"chicken (?:stock|stock powder|broth|bouillon|granule|juice|consomme|veloute|base|soup base)(?: powder)?"
            ],
            "vegetable stock": [
                r"(?:vegetable|veggie|veg) stock",
                r"(?:vegetable|veggie|veg) stock powder",
                r"(?:vegetable|veggie|veg) broth",
                r"(?:vegetable|veggie|veg) bouillon",
                r"(?:vegetable|veggie|veg) bouillon powder",
                r"(?:vegetable|veggie|veg) granule",
                r"(?:vegetable|veggie|veg) juice",
                r"v8(?: vegetable| veggie| veg)? juice",
                r"v8",
            ],
            "beef stock": [
                r"beef (?:stock|stock powder|broth|bouillon|granule|juice|consomme|veloute|base|soup base)(?: powder)?"
            ],
            "fish stock": [
                r"dashi",
                r"bonito stock",
                r"(?:fish|seafood|crab|mussel) (?:stock|stock powder|broth|bouillon|granule|juice|consomme|veloute)(?: powder)?"
            ],
            "pork stock": [
                r"pork (?:stock|stock powder|broth|bouillon|granule|juice|consomme|veloute)(?: powder)?"
            ],
            "bouillon cube": [r"bouillon cube", r"bouillon granule", r"stock cube"],
            "stock": [r"(?:stock|stock powder|broth|bouillon|granule|consomme|veloute)(?: powder)?"],
            "chicken soup": [r"chicken soup"],
            "mushroom soup": [r"mushroom soup"],
            "onion soup": [r"onion soup"],
            "tomato soup": [r"tomato soup"],
            "vegetable soup": [r"potato soup", r"vegetable soup", r"celery soup"],
            "soup mix": [r"soup mix"],
            "soup": [r"soup", r"bisque", r"chowder", r"stew"],
        },
        "ALCOHOL": {
            "irish cream": [r"irish cream", r"bailey's"],
            "beer": [r"\bbeer", r"\bale", r"\bstout", r"lager"],
            "whiskey": [r"whiske?y", r"scotch"],
            "vodka": [r"\bvodka"],
            "cider": [r"c[iy]der"],
            "citrus liqueur": [r"limoncello", r"orange liqueur", r"margarita mix"],
            "fruit liqueur": [r"amaretto", r"curacao"],
            "liqueur": [
                r"rumchata",
                r"\brum",
                r"spirit",
                r"rum extract",
                r"liqueur",
                r"liquor",
                r"cachaca",
                r"calvados?",
                r"creme de cacao",
                r"frangelico",
                r"rum",
                r"amarula cream liqueur",
                r"ouzo",
                r"kirsch",
                r"bourbon",
                r"brandy",
                r"gin",
                r"kahlua",
                r"grand marnier",
                r"cognac",
                r"triple sec",
                r"vodka",
                r"tequila",
                r"brandy",
                r"bitters?",
                r"cointreau",
                r"schnapps?",
                r"cachaca",
                r"eggnog",
                r"campari",
                r"bourbon",
                r"galliano",
                r"pernod",
                r"creme the menthe",
                r"drambuie",
                r"creme de cassis",
                r"tia maria",
                r"cordial",
                r"armagnac",
            ],
            "fortified wine": [
                r"marsala(?: wine)?",
                r"madeira(?: wine)?",
                r"port wine",
                r"mistell?a wine",
                r"\bport",
                r"vermouth",
                r"sherry wine",
                r"sherry",
            ],
            "rice wine": [
                r"shaoxing wine",
                r"rice wine",
                r"cooking wine",
                r"^sake",
                r"chinese wine",
                r"mirin",
            ],
            "red wine": [r"\bred wine", r"merlot"],
            "white wine": [r"white wine", r"prosecco", r"champagne", r"wine"],
        },
        "_liquid": [r"liquid", r"fluid", r"juice", r"beverage"],
    },
    "VINEGAR & ACIDS": {
        "vinaigrette": [r"vinaigrette"],
        "wine vinegar": [r"wine vinegar"],
        "cider vinegar": [r"c[iy]der vinegar"],
        "balsamic vinegar": [r"balsamic vinegar"],
        "rice vinegar": [r"rice vinegar"],
        "pickle juice": [r"pickle juice", r"jalapeno juice", r"pickling juice"],
        "vinegar": [r"vinegar"],
    },
    "SEAWEED": {
        "GREEN SEAWEED": {
            "umibudo": [r"umi ?budo", r"sea grapes?", r"green caviar"],
            "sea lettuce": [r"sea lettuce", r"green laver"],
        },
        "BROWN SEAWEED": {
            "wakame": [r"wakame(?: seaweed)?"],
            "arame": [r"arame(?: seaweed)?"],
            "hiijiki": [r"hiijiki(?: seaweed)?"],
            "kombu": [r"kombu(?: seaweed)?", r"konbu", r"kelp"],
        },
        "RED SEAWEED": {
            "dulse": [r"dulse(?: seaweed)?", r"dillisk"],
            "nori": [r"nori(?: seaweed)?", r"laver"],
            "carrageenan": [r"carrageenan"],
        },
    },
    "NICHE": {
        "jam": [
            r"jam",
            r"jelly",
            r"preserves?",
            r"fruit spread",
            r"marm[ea]lade",
            r"confiture",
        ],
        "puree": [r"puree"],
        "chutney": [r"chutney(?: relish| sauce)?", r"piccalilli"],
        "crouton": [r"croutons?"],
        "vegemite": [r"vegemite", r"marmite"],
        "granola": [r"granola", r"granola cereal"],
        "corn flakes": [r"corn ?flakes?( crumbs?| cereal)?"],
        "marshmallow": [r"marshmallows?", r"marshmallow fluff"],
        "stuffing": [r"stuffing mix", r"stuffing"],
        "filling": [r"filling"],
        "topping": [r"topping"],
        "dressing": [r"dressing(?: mix)?"],
        "miso": [r"\bmiso", r"soybean paste", r"miso paste"],
        "yeast": [r"yeast"],
        "gravy": [r"\bgravy", r"gravy mix"],
        "bone": [r"\bbones?"],
        "liquid smoke": [r"liquid smoke"],
        "pickle": [
            r"pickle",
            r"gherkin",
            r"pickled cucumber",
            r"cornichon",
            r"relish",
        ],
        "coleslaw": [r"coleslaw", r"coleslaw mix"],
        "pico de gallo": [r"pico de gallo"],
        "tortilla chip": [r"tortilla chip", r"corn chip"],
        "breadcrumb": [r"bread ?crumbs?", r"panko"],
        "raisin": [r"sultanas?", r"raisins?"],
        "cream of tartar": [r"cream tartar", r"potassium bitartrate"],
        "ice": [r"ice cube", r"\bice"],
    },
    "TOOLS": {
        "parchment paper": [r"parchment paper", r"baking paper"],
        "toothpick": [r"toothpick"],
        "foil": [r"foil", r"aluminum foil"],
        "skewer": [r"skewer"],
    },
    "THICKENING AGENTS": {
        "gelatin": [r"gelatine?(?: powder)?", r"agar agar(?: powder)?"],
        "xanthan gum": [r"xanthan gum"],
        "starch": [
            r"starch",
            r"cornstarch",
            r"pectin",
        ],
        "_thickening agent": [r"thickening agent", r"thickener"],
    },
    "PROTEIN": {
        "SEAFOOD": {
            "FISH": {
                "LEAN FISH": {
                    "carp": [r"carp"],
                    "bonita": [r"bonita"],
                    "bass": [r"bass"],
                    "squeteague": [r"squeteague"],
                    "catfish": [r"catfish"],
                    "flounder": [r"flounder"],
                    "cod": [r"cod"],
                    "skrei": [r"skrei"],
                    "hake": [r"hake"],
                    "hoki": [r"hoki"],
                    "sole": [r"sole"],
                    "snapper": [r"snapper"],
                    "perch": [r"perch"],
                    "haddock": [r"haddock"],
                    "halibut": [r"halibut"],
                    "greenland turbot": [r"greenland turbot"],
                    "pike": [r"pike"],
                    "tilapia": [r"tilapia"],
                    "swai": [r"swai"],
                    "whitefish": [r"whitefish"],
                    "mahi mahi": [r"mahi[- ]?mahi"],
                    "barramundi": [r"barramundi"],
                    "char": [r"(?<!arctic )char"],
                    "trout": [r"trout"],
                    "pollock": [r"pollock"],
                    "cobia": [r"cobia"],
                    "croaker": [r"croaker"],
                    "mullet": [r"mullet"],
                    "rockfish": [r"rockfish"],
                    "whiting": [r"whiting"],
                    "saury": [r"saury"],
                    "plaice": [r"plaice"],
                    "grenadier": [r"grenadier"],
                    "kingklip": [r"kingklip"],
                    "sanddab": [r"sanddab"],
                    "sandperch": [r"sandperch"],
                    #
                    "_lean fish": [r"lean fish"],
                },
                "FATTY FISH": {
                    "herring": [r"herring"],
                    "eel": [r"eel"],
                    "trout": [r"trout"],
                    "arctic char": [r"arctic char"],
                    "butterfish": [r"butterfish"],
                    "mackerel": [r"mackerel"],
                    "anchovy": [r"^anchov(?:y|ies)"],
                    "sardine": [r"sardines?"],
                    "swordfish": [r"swordfish"],
                    "shark": [r"shark"],
                    "monkfish": [r"monk[- ]?fish"],
                    "bluefish": [r"bluefish"],
                    "wahoo": [r"wahoo"],
                    "turbot": [r"(?<!greenland )turbot"],
                    #
                    "salmon": [r"salmon"],
                    "tuna": [r"tuna"],
                    #
                    "_fatty fish": [r"fatty fish", r"oily fish"],
                },
                "_fish": [r"fish"],
            },
            "SHELLFISH": {
                "CRUSTACEANS": {
                    "lobster": [r"lobsters?", r"lobsterette?s?"],
                    "langoustine": [r"langoustines?"],
                    "crab": [r"crabs?", r"crabmeat", r"crabmeat blend"],
                    "shrimp": [r"shrimps?", r"prawns?"],
                    "crawfish": [r"cra[wy][ -]?(?:fish|daddy|dad)"],
                    #
                    "_crustacean": [r"crustaceans?"],
                },
                "MOLLUSKS": {
                    "clam": [r"clams?"],
                    "oyster": [r"oysters?"],
                    "mussel": [r"mussels?"],
                    "scallop": [r"scallops?"],
                    "cockle": [r"cockles?"],
                    "abalone": [r"abalones?"],
                    "conch": [r"conch(?:es)?"],
                    "whelk": [r"whelks?"],
                    "periwinkle": [r"periwinkles?"],
                    "snail": [r"snails?", r"escargots?"],
                    #
                    "_mollusk": [r"mollusks?"],
                },
                #
                "_shellfish": [r"shellfish"],
            },
            "CEPHALOPODS": {
                "squid": [r"squid"],
                "octopus": [r"octopus"],
                "calamari": [r"calamari"],
                "cuttlefish": [r"cuttle[- ]?fish"],
            },
            "OTHER": {
                "roe": [r"roe", r"caviar", r"tobiko", r"ikura"],
                "bonito flakes": [r"bonito flakes", r"katsuobushi"], 
            },
        },
        "MEAT": {
            "WHITE MEAT": {
                "chicken": [
                    r"chickens?",
                    r"hens?",
                    r"poussins?",
                    r"capons?",
                    r"roosters?",
                ],
                "turkey": [r"turkeys?"],
                "alligator": [r"alligators?"],
                "crocodile": [r"crocodiles?"],
                "rabbit": [r"rabbits?", r"bunn(?:y|ies)", r"hares?"],
                "squirrel": [r"squirrels?"],
            },
            "HAM & BACON": {
                "ham": [
                    r"mortadellas?",
                    r"\bhams?",
                    r"pancetta(?: (?:di )?cubetti)?",
                    r"prosciutto",
                    r"jamon(?: iberico)?",
                    r"jambon",
                    r"capicola",
                    r"culatello",
                    r"gammon",
                    r"serrano",
                    r"bresaola",
                    r"lomo",
                ],
                "bacon": [
                    r"bacon bits?",
                    r"bacon",
                    r"lardons?",
                    r"rashers?",
                    r"speck",
                    r"guanciale",
                    r"szalonna",
                    r"lap yuk",
                ],
            },
            "RED MEAT": {
                "CATTLE": {
                    "bison": [r"bison"],
                    "buffalo": [r"buffalo"],
                    "beef": [
                        r"beef",
                        #
                        r"new york strip",
                        r"cow",
                        r"entrec[oô]te",
                        r"fill?et mignon",
                        r"loin",
                        r"tenderloin",
                        r"sirloin",
                        r"wagyu",
                        r"rib[ \-]eye",
                        r"beef",
                        r"oxtail",
                        r"steak",
                        r"ground meat",
                        r"mincemeat",
                        r"stew meat",
                        r"minced meat",
                        r"meat",
                        r"roast",
                        r"^chuck",
                        r"hamburger",
                        r"round",
                    ],
                },
                "OTHER": {
                    "veal": [r"veal"],
                    "lamb": [r"lamb", r"mutton", r"hogget"],
                    "pork": [r"pork", r"pig", r"swine", r"hog"],
                },
            },
            "GAME": {
                "WINGED GAME": {
                    "pigeon": [r"pigeon", r"squab"],
                    "quail": [r"quail"],
                    "partridge": [r"partridge"],
                    "crane": [r"cranes?"],
                    "goose": [r"gooses?"],
                    "duck": [r"ducks?"],
                    "pheasant": [r"pheasants?"],
                    "grouse": [r"grouses?"],
                    "guinea fowl": [r"guinea fowls?"],
                    "woodcock": [r"woodcocks?"],
                    "teal": [r"teals?"],
                    "snipe": [r"snipes?"],
                    "thrush": [r"thrushs?"],
                    "starling": [r"starlings?"],
                    "lapwing": [r"lapwings?"],
                },
                "BIG GAME": {
                    "goat": [r"goats?"],
                    "venison": [
                        r"venisons?",
                        r"deers?",
                        r"elks?",
                        r"mooses?",
                        r"caribous?",
                        r"antelopes?",
                        r"pronghorns?",
                        r"reindeers?",
                    ],
                    "boar": [r"boars?"],
                    "kangaroo": [r"kangaroos?"],
                    "bear": [r"bears?"],
                    "ostrich": [r"ostrich"],
                    "emu": [r"emu"],
                },
            },
            "SAUSAGE": {
                "cured sausage": [
                    r"salamis?",
                    r"pepperonis?",
                    r"longanizas?",
                    r"longganisas?",
                ],
                "liver sausage": [
                    r"liverwurst",
                    r"braunschweiger",
                    r"liver sausage",
                    r"liver pate",
                ],
                "blood sausage": [
                    r"black[- ]?pudding",
                    r"white[- ]?pudding",
                    r"morcilla",
                ],
                "sausage": [
                    r"bangers?",
                    r"sausage(?:s|meat)?",
                    r"chorizos?",
                    r"kielbasas?",
                    r"bratwursts?",
                    r"sai[- ]?ua",
                    r"sai kok",
                    r"chipolatas?",
                    r"boudins?",
                    r"salchichas?",
                    r"dogs?",
                    r"frankfurters?",
                ],
            },
            "INNARDS": {
                "liver": [r"livers?"],
                "kidney": [r"kidneys?"],
                "heart": [r"hearts?"],
                "tongue": [r"tongues?"],
                "sweetbread": [r"sweetbreads?"],
                "tripe": [r"tripes?"],
                "brain": [r"brains?"],
                "head": [r"head"],
                "ear": [r"ears?"],
                "snout": [r"snouts?"],
                "gizzard": [r"gizzards?"],
                "testicle": [r"testicles?"],
            },
        },
        "OTHER": {
            "tofu": [r"tofu"],
            "tempeh": [r"tempeh"],
            "seitan": [r"seitan"],
            "quorn": [r"quorn"],
            "mock meat": [r"mock meat"],
        },
    },
}


# a function that yields all the deepest keys in a dictionary and a list of the keys that lead to them
def _get_deepest_keys(d, path=[]):
    if isinstance(d, dict):
        for k, v in d.items():
            yield from _get_deepest_keys(v, path + [k])
    else:
        yield d, path[:-1], path[-1]


for regex, path, ingredient in _get_deepest_keys(_nested_dictionary):
    # loop through ingredients and create a IngredientFamily structure
    cookbook.register_ingredient(ingredient, regex, path)