import random


class Channel:
    """docstring for Channel

    The index of the first bit is zero.

    description examples:
        4          changes 4 bits in the full bit sequence
        "4"        same as the previous
        "num=4"    same as the previous
        "2-4" changes 2, 3 or 4 bits in the full bit sequence
        "4/8"  changes four bits for every 8 bits
        "2-4/8"  combination of the previous two
        "bits=0,2,-1" changes the bits 0, 1, and last
        [0,2,-1]      as the previous
        "ber=0.1"  bit error rate = 0.1
        0.1        as in previous
    """
    def __init__(self, description, **kwargs):
        if isinstance(description, int):
            description = str(description)
        if isinstance(description, list):
            for i in description:
                assert isinstance(i, int)
            description = "bits={0}".format(
                ",".join(str(b) for b in description)
            )
        if isinstance(description, float):
            assert 0 <= description < 1
            description = "ber={0}".format(description)
        self.description = description
        splitted = description.split("=")
        assert len(splitted) in (1, 2)
        if len(splitted) == 1:
            self.type = "num"
            self.value = description
        else:
            self.type, self.value = splitted
        self.value = self.value.strip()
        assert self.type in ["num", "ber", "bits"]
        assert isinstance(self.value, str)

    def run(self, input_):
        if self.type == "num":
            if "/" not in self.value:
                interval = self.value
            else:
                raise NotImplementedError
            if "-" not in interval:
                bit_error_num = int(interval)
            else:
                min_, max_ = interval.split("-")
                bit_error_num = random.randint(int(min_), int(max_))
            errors = random.sample(range(len(input_)), bit_error_num)
        elif self.type == "ber":
            self.value = float(self.value)
            assert self.value <= 1,\
                "bit error rate must be less or equal than 1"
            errors = [i for i in range(len(input_))
                      if random.random() < float(self.value)]
        elif self.type == "bits":
            errors = [(int(i) - 1) for i in self.value.split(",")]
        return input_.flip_bits(errors)

    def verbose_description(self):
        if self.type == "num":
            interval = self.value
            if "-" in interval:
                return "csatorna {interval[0]} és {interval[1]}"\
                    " közötti hibával".format(interval=interval.split("-"))
            else:
                if self.value in ['0', 0]:
                    return "hibamentes csatorna"
                else:
                    return "csatorna {} hibával".format(self.value)
        if self.type == "ber":
            return \
                "csatorna, amely a bitek {} részét elrontja".format(self.value)
        if self.type == "bits":
            return "csatorna, amely a következő"\
                " biteket elrontja: {}".format(self.value)

    def __repr__(self):
        return 'Channel("{0}={1}")'.format(self.type, self.value)
