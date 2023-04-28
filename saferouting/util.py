import heapq


class FHeap:
    def __init__(self):
        self.f_values = {}
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def insert(self, id, val):
        if id in self.f_values:
            if self.f_values[id] > val:
                for i in range(len(self.heap)):
                    if self.heap[i][1] == id:
                        self.heap.pop(i)
                        break
                self.f_values[id] = val
                heapq.heappush(self.heap, (val, id))
        else:
            self.f_values[id] = val
            heapq.heappush(self.heap, (val, id))

    def pop(self):
        _, id = heapq.heappop(self.heap)
        self.f_values.pop(id)
        return id

    def heapify(self):
        heapq.heapify(self.heap)
