
class MinHeap:

    def __init__(self):
        self.items = []

    def __len__(self):
        return len(self.items)

    def peek(self):
        return self.items[0]

    def push(self, value):
        self.items.append(value)
        self._sift_up(len(self.items) - 1)

    def replace_top(self, value):
        self.items[0] = value
        self._sift_down(0)

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.items[index] >= self.items[parent]:
                break
            self.items[index], self.items[parent] = self.items[parent], self.items[index]
            index = parent

    def _sift_down(self, index):
        size = len(self.items)
        while True:
            left = 2 * index + 1
            right = left + 1
            smallest = index

            if left < size and self.items[left] < self.items[smallest]:
                smallest = left
            if right < size and self.items[right] < self.items[smallest]:
                smallest = right
            if smallest == index:
                break

            self.items[index], self.items[smallest] = self.items[smallest], self.items[index]
            index = smallest