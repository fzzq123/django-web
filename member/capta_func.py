import random
import string


def random_digit_challenge():
    """生成 6 位随机数字验证码"""
    ret = ''
    for i in range(6):
        ret += str(random.randint(0, 9))
    return ret, ret


def random_alphanumeric_challenge():
    """生成 4-6 位随机字母+数字混合验证码（练习用）"""
    length = random.randint(4, 6)
    chars = string.ascii_letters + string.digits
    ret = ''.join(random.choice(chars) for _ in range(length))
    return ret, ret
