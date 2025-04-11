import time
import lucene
import src.csv_related as csv_related
import src.lyrics_processing as lyr_proc
import src.gui as gui
import src.lucene_engine as lucene_engine

def init_lucene_vm():
    try:
        lucene.initVM()
        print("Lucene version:", lucene.VERSION)

    except Exception as e:
        print("Error initializing Lucene VM:", e)

def init():

    t1 = time.time()
    csv_related.main()  # beautify the csv files before the text processing

    lyr_proc.repeat_lyrics("lyrics", "lyrics")  # repeat lyrics, remove brackets, stemming
    
    lucene_engine.init_lucene()

    t2 = time.time() - t1
    print(f"It took {t2}secs")

    gui.init_gui()


if __name__ == "__main__":
    init_lucene_vm()
    init()
