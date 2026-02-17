from local_align import *
from collections import defaultdict

class SentenceAligner:

    def __init__(self):

        pass

    def border_align(self, text_a, text_b, identifier):

        #print(text_a)
        #print(text_b)
        align_a = "^" + text_a.lower() + "$"
        align_b = "^" + text_b.lower() + "$"
        words_a = text_a.split(" ")
        words_b = text_b.split(" ")
        if text_a.lower() == text_b.lower():
            map_list = [(w,w) for w in words_a]
            return {'words_a' : words_a, 'words_b' : words_b, 'mapping' : map_list}
        A = local_align(align_a, align_b)
        AL = all_alignment(A, align_a, align_b)

        #word_boundaries = [(a[0], a[1], i) for i, a in enumerate(AL) if a[0] is not None and a[1] is not None and  align_a[a[0]] == " " and align_b[a[1]] == " "]
        word_boundaries = [(a[0], a[1], i, " ") if a[1] is not None and align_b[a[1]] == " " else (a[0], a[1], i, None) for i, a in enumerate(AL) if a[0] is not None and align_a[a[0]] == " "]
        x = 1
        y = 1
        mapping = {-1 : []}
        a_id = 0
        b_id = 0
        bound_id = 1
        prev_boundary = None

        #print(AL)
        #print(word_boundaries)
        #print(text_a)
        #print(text_b)
        x = 1
        a_buffer = []
        a_id_buffer = []
        map_list = []
        for wb in word_boundaries+[(len(align_a)-1, len(align_b)-1, len(AL), '$')]:
            a_word = "".join([align_a[z[0]] for z in AL[x:wb[2]] if z[0] is not None])
            a_buffer.append(a_word)
            if wb[3] is None:
                x = wb[2]+1
                continue
            b_word = "".join([align_b[z[1]] for z in AL[y:wb[2]] if z[1] is not None])
            #print(" ".join(a_buffer+[a_word]), wb, b_word)
            map_list.append((a_buffer, b_word.split(" ")))

            a_buffer = []
            a_id_buffer = []
            x = wb[2]+1
            y = wb[2]+1

        return {'words_a' : words_a, 'words_b' : words_b, 'mapping' : map_list}

    def multi_align(self, *alignment_data):

        primary_map = {}
        secondary_map = {}
        for i, data in enumerate(alignment_data):
            #print(i, data)
            a_id = 0
            b_id = 0
            words_a = data['words_a']
            words_b = data['words_b']
            al = data['mapping']
            for row in al:
                a_side = row[0]
                b_side = row[1]

                if len(a_side) == 1:
                    if a_id not in primary_map:
                        primary_map[a_id] = defaultdict(int)
                    if len(b_side) == 1:
                        primary_map[a_id][words_b[b_id].lower()] += 1
                    elif len(b_side) > 1:
                        b_key = tuple(words_b[b_id:b_id+len(b_side)])
                        #primary_map[a_id][(b_id, b_id+len(b_side)-1)] += 1
                        primary_map[a_id][b_key] += 1
                    b_id += len(b_side)
                    a_id += 1
                elif len(a_side) > 1:
                    secondary_key = tuple([a_id,a_id+len(a_side)-1])
                    #secondary_key = (a_id, a_id+len(a_side)-1)
                    if secondary_key not in secondary_map:
                        secondary_map[secondary_key] = defaultdict(int)
                    secondary_map[secondary_key][words_b[b_id]] += 1
                    a_id += len(a_side)
                    b_id += 1

        return {'primary' : dict(primary_map), 'secondary' : dict(secondary_map)}

if __name__ == '__main__':

    SA = SentenceAligner()

    #SA.border_align("apple pear banana", "apple pear banana", 1)
    #SA.border_align("apple par banana", "apple pear banana", 1)
    ##SA.border_align("i apple par banana", "apple pear banana", 1)
    #SA.border_align("apple par banana", "i apple pear banana", 1)
    #SA.border_align("apple par banana", "apple i pear banana", 1)
    #SA.border_align("apple par banana", "apple pear banana i", 1)
    #SA.border_align("i apple pear banana", "i applepear banana", 1)
    #SA.border_align("i applepear banana", "i apple pear banana", 1)
    #SA.border_align("and estates here after limitted from being defeated or", "and estates hereinafter limited from being defeated or", 1)
    A1 = SA.border_align("and estates hereinafter limitted from being defeated or", "and estates here after limited from being defeated or", 1)
    A2 = SA.border_align("and estates hereinafter limitted from being defeated or", "and estates here after limited from being defeated or", 1)
    A3 = SA.border_align("and estates hereinafter limitted from being defeated or", "and estates here after limi ted from being defeated or", 1)
    A1 = SA.border_align("and estates here after limitted from being defeated or", "and estates hereinafter limited from being defeated or", 1)
    A2 = SA.border_align("and estates here after limitted from being defeated or", "and estates hereinafter limited from being defeated or", 1)
    A3 = SA.border_align("and estates here after limitted from being defeated or", "and estates hereinafter limi ted from being defeated or", 1)
    MA = SA.multi_align(A1, A2, A3)
    print(MA)

    #SA.border_align("iguana par banana", "iguna apple pear banana")
    #SA.border_align("iguana apple par banana", "iguna applepear banana")
