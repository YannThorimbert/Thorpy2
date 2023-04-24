import time
class Monitor:

    def get_n_iterations(self, letter):
        return len(getattr(self,letter))

    def append(self, name):
        if not hasattr(self, name):
            setattr(self, name, [time.perf_counter()])
        else:
            getattr(self,name).append(time.perf_counter())

    def reset(self):
        for letter in "abcdefghijklmnopqrstuvwxyz":
                if hasattr(self,letter):
                    setattr(self, letter, [])

    def autocomplete(self):
        lengths = []
        lengths_dict = {}
        all_letters = self.list_letters()
        for letter in all_letters:
            n = len(getattr(self,letter))
            lengths.append(n)
            lengths_dict[letter] = n
        L = max(lengths)
        for i in range(1,len(all_letters)):
            letter = all_letters[i]
            letter_prev = all_letters[i-1]
            n = lengths_dict[letter]
            if n < L:
                for i in range(n, L):
                    time_prev_letter = getattr(self, letter_prev)[i]
                    getattr(self,letter).append(time_prev_letter)

    def list_letters(self):
        letters = []
        for letter in "abcdefghijklmnopqrstuvwxyz":
            if hasattr(self,letter):
                letters.append(letter)
        return letters

    def show(self, letters=None, rnd=None):
        if not letters:
            letters = self.list_letters()
        n_lett = len(letters)
        tot = [0.]*n_lett
        L = len(getattr(self,letters[0]))
        print("Stats over", L, "iterations:")
        for i in range(1,n_lett):
            for k in range(L): #k is the iteration
                letter_i = getattr(self,letters[i])
                letter_j = getattr(self,letters[i-1])
                if len(letter_i) <= k:
                    raise Exception("Letter "+str(letters[i])+" not called each frame")
                if len(letter_j) <= k:
                    raise Exception("Letter "+str(letters[i-1])+" not called each frame")
                diff = letter_i[k] - letter_j[k]
                tot[i] += diff
        for k in range(1,L): #z->a_previous_iteration
            diff = getattr(self,letters[0])[k] - getattr(self,letters[n_lett-1])[k-1]
            tot[0] += diff
        for i in list(range(1,len(tot)))+[0]: #we want z->a displayed at the end
            if rnd is None:
                n = tot[i]
            else:
                n = round(tot[i], rnd)
            p = round(100*n/sum(tot))
            print(letters[i-1]+"->"+letters[i]+": "+str(round(n,6))+" ("+str(p)+"%)")