import constants

def main():
    key = input("move or undo: ")

    if "move" in key.lower():
        # constants.undo(constants.from_, constants.end_library)
        # constants.undo(constants.from_, constants.start_library)
        constants.categorize(constants.from_, constants.start_library)
        constants.categorize(constants.from_, constants.end_library)
        # constants.transfer(constants.from_, constants.to, constants.end_library)
    # if "undo" in key.lower():
    #     # constants.transfer(constants.to, constants.from_, constants.end_library)
    #     # constants.undo(constants.from_, constants.end_library)
    #     constants.undo(constants.from_, constants.start_library)

if __name__ == "__main__":
    main()