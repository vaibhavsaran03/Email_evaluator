from generator.generate import generate_responses

from evaluation.evaluate import evaluate


def main():

    print()

    print("=" * 50)

    print("Generating Responses...")

    generate_responses()

    print()

    print("=" * 50)

    print("Evaluating Responses...")

    evaluate()

    print()

    print("=" * 50)

    print("Done.")

    print()


if __name__ == "__main__":
    main()