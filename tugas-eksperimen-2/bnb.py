'''
Code for the unbounded knapsack problem using branch and bound approach
is taken from https://www.tandfonline.com/doi/pdf/10.1057/palgrave.jors.2601698?casa_token=EW35GGben2sAAAAA%3AVZt6DkysIcc7im289FIjHbV6Q3nZr2vYAH_HtWInlRnwryJnWsXKK87_g478Gof5mB_MDiz29IDO1eA

The pseudocode inside the PDF is then refactored to Python.
PDF is "An improved branch and bound algorithm for a strongly correlated unbounded knapsack problem"
by Y-J Seong, Y-G G, M-K Kang & C-W Kang

PDF is also included in this repository as reference.
'''

import math
from enum import Enum

class SearchState(Enum):
    COMPLETE = 1
    RETRACE = 2
    PROCEED = 3

class KnapsackOptimizer:
    def __init__(self, capacity, weights, values):
        self.capacity = capacity
        self.items = [{'value': values[i], 'weight': weights[i]} for i in range(len(weights))]
        self.num_items = len(self.items)
        self.memory_table = None
        self.optimal_solution = None
        self.optimal_value = None

    def eliminate_dominated_items(self):
        self.items.sort(key=lambda item: item['value'] / item['weight'], reverse=True)
        superior_items = []

        for current_item in self.items:
            if not any(other['weight'] <= current_item['weight'] and other['value'] >= current_item['value'] for other in superior_items):
                superior_items.append(current_item)

        self.items = superior_items
        self.num_items = len(superior_items)

    def compute_upper_bound(self, remaining_capacity, accumulated_value, index):
        if index + 2 < self.num_items:
            item1, item2, item3 = self.items[index:index+3]
            return self.estimate_bound(remaining_capacity, accumulated_value, item1, item2, item3)
        else:
            return accumulated_value

    def estimate_bound(self, remaining_capacity, accumulated_value, item1, item2, item3):
        base_value = accumulated_value + (remaining_capacity // item2['weight']) * item2['value']
        new_capacity = remaining_capacity - (remaining_capacity // item2['weight']) * item2['weight']
        first_bound = base_value + (new_capacity * item3['value'] // item3['weight'])

        adjusted_capacity = new_capacity + math.ceil((1 / item1['weight']) * (item2['weight'] - new_capacity)) * item1['weight']
        second_bound = base_value + math.floor((adjusted_capacity * item2['value'] / item2['weight']) - math.ceil((1 / item1['weight']) * (item2['weight'] - new_capacity)) * item1['value'])

        return max(first_bound, second_bound)

    def initialize_search(self):
        self.eliminate_dominated_items()
        self.memory_table = [[0 for _ in range(self.capacity + 1)] for _ in range(self.num_items)]
        self.optimal_solution = [0 for _ in range(self.num_items)]
        self.optimal_value = 0

        selection = [0 for _ in range(self.num_items)]
        current_index = 0
        selection[0] = self.capacity // self.items[0]['weight']
        current_value = self.items[0]['value'] * selection[0]
        remaining_capacity = self.capacity - self.items[0]['weight'] * selection[0]
        upper_bound = self.compute_upper_bound(remaining_capacity, current_value, current_index)
        self.optimal_value = current_value
        self.optimal_solution = selection.copy()

        minimum_weights = [min(item['weight'] for item in self.items[i + 1:]) for i in range(self.num_items - 1)] + [float('inf')]
        return selection, current_index, current_value, remaining_capacity, upper_bound, minimum_weights

    def search(self, selection, current_index, current_value, remaining_capacity, upper_bound, minimum_weights):
        if remaining_capacity < minimum_weights[current_index]:
            return self.evaluate_solution(selection, current_index, current_value, remaining_capacity, upper_bound)
        
        next_item = self.find_next_item(current_index, remaining_capacity)
        if next_item is None or self.memory_table[current_index][remaining_capacity] >= current_value:
            return selection, current_index, current_value, remaining_capacity, SearchState.RETRACE
        
        return self.update_selection(selection, current_index, current_value, remaining_capacity, next_item)

    def evaluate_solution(self, selection, current_index, current_value, remaining_capacity, upper_bound):
        if self.optimal_value < current_value:
            self.optimal_value = current_value
            self.optimal_solution = selection.copy()
            if self.optimal_value == upper_bound:
                return selection, current_index, current_value, remaining_capacity, SearchState.COMPLETE
        return selection, current_index, current_value, remaining_capacity, SearchState.RETRACE

    def find_next_item(self, current_index, remaining_capacity):
        return next((j for j in range(current_index + 1, self.num_items) if self.items[j]['weight'] <= remaining_capacity), None)

    def update_selection(self, selection, current_index, current_value, remaining_capacity, next_item):
        selection[next_item] = remaining_capacity // self.items[next_item]['weight']
        current_value += self.items[next_item]['value'] * selection[next_item]
        remaining_capacity -= self.items[next_item]['weight'] * selection[next_item]
        self.memory_table[current_index][remaining_capacity] = current_value
        return selection, next_item, current_value, remaining_capacity, SearchState.PROCEED

    def backtrack_search(self, selection, current_index, current_value, remaining_capacity, minimum_weights):
        prev_item = max((j for j in range(current_index + 1) if selection[j] > 0), default=None)
        if prev_item is None:
            return selection, current_index, current_value, remaining_capacity, SearchState.COMPLETE
        
        return self.adjust_selection(selection, prev_item, current_value, remaining_capacity, minimum_weights)

    def adjust_selection(self, selection, prev_item, current_value, remaining_capacity, minimum_weights):
        selection[prev_item] -= 1
        current_value -= self.items[prev_item]['value']
        remaining_capacity += self.items[prev_item]['weight']

        if remaining_capacity < minimum_weights[prev_item]:
            return selection, prev_item, current_value, remaining_capacity, SearchState.RETRACE

        if current_value + math.floor(remaining_capacity * self.items[prev_item + 1]['value'] / self.items[prev_item + 1]['weight']) <= self.optimal_value:
            current_value -= self.items[prev_item]['value'] * selection[prev_item]
            remaining_capacity += self.items[prev_item]['weight'] * selection[prev_item]
            selection[prev_item] = 0
            return selection, prev_item, current_value, remaining_capacity, SearchState.RETRACE
        
        return selection, prev_item, current_value, remaining_capacity, SearchState.PROCEED

    def execute_branch_and_bound(self):
        selection, current_index, current_value, remaining_capacity, upper_bound, minimum_weights = self.initialize_search()
        next_step = SearchState.PROCEED
        while next_step != SearchState.COMPLETE:
            if next_step == SearchState.PROCEED:
                selection, current_index, current_value, remaining_capacity, next_step = self.search(selection, current_index, current_value, remaining_capacity, upper_bound, minimum_weights)
            elif next_step == SearchState.RETRACE:
                selection, current_index, current_value, remaining_capacity, next_step = self.backtrack_search(selection, current_index, current_value, remaining_capacity, minimum_weights)
        return self.optimal_solution, self.optimal_value


if __name__ == '__main__':
    W = 100
    val = [10, 30, 20]
    wt = [5, 10, 15]

    optimizer = KnapsackOptimizer(W, wt, val)
    solution, value = optimizer.execute_branch_and_bound()
    print(value)
