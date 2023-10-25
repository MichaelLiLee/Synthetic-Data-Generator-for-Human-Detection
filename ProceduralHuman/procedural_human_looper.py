## prevent create __pycache__ file
import sys
sys.dont_write_bytecode = True
from procedural_human import ProceduralHuman


def gen_one_human():
    procedural_human = ProceduralHuman()
    procedural_human.random_open_base_model_then_randomize()

if __name__ == "__main__":

    gen_human = 500
    for i in range(gen_human):
        gen_one_human()
        print(f'Already Gen {i} Humans , {gen_human - i} ToGo!')
