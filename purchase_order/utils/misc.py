import random
import string


def generate_crpto_accurate_keys():
    """
    Generate a random 8 character string
    :return:
    """
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
