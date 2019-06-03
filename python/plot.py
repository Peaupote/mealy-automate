import sys
import matplotlib.pyplot as plt


def plot(file):
    f = open(file, "rb")

    plt.figure(1)
    c = 0
    while True:
        c += 1
        print(c)
        byte_size = f.read(4)
        if not byte_size:
            f.close()
            break
        size = int.from_bytes(byte_size, byteorder='little', signed=False)
        x = list(range(size-1))
        trivial = True if int.from_bytes(
            f.read(4), byteorder='little', signed=False) == 1 else False
        y = []
        for _ in range(size-1):
            y.append(int.from_bytes(
                f.read(4), byteorder='little', signed=False))

        if trivial:
            plt.subplot(1, 2, 1)
        else:
            plt.subplot(1, 2, 2)
        plt.plot(x, y)

    plt.show()


if __name__ == "__main__":
    plot(sys.argv[1])
