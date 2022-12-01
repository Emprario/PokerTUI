def create_cards():
    directory = "assets/cmi/"
    default_dir = "assets/samples/"
    default_basename = "_default_"
    couleurs = ("carreau", "coeur", "pique", "trefle")
    figure = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K",
              "As")
    extension = ".cmi"

    for card in [(c, f) for f in figure for c in couleurs]:
        with open(default_dir + default_basename + card[0] + extension,
                  'r') as default:
            txt = default.readlines()
        if len(card[1]) == 2:
            txt[2] = txt[2][:3] + card[1] + txt[2][5:]
            txt[9] = txt[9][:9] + card[1] + txt[9][11:]
        elif len(card[1]) == 1:
            txt[2] = txt[2][:3] + card[1] + " " + txt[2][5:]
            txt[9] = txt[9][:9] + " " + card[1] + txt[9][11:]
        filename = card[0] + card[1] + extension
        with open(directory + filename, 'w') as cmi:
            cmi.write("".join(txt))
