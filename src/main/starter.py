from analyze_text.text_preprocessor import  TextPreprocessor

def run():
    preprocessor = TextPreprocessor()
    preprocessor.preprocess_files()

if __name__=="__main__":
    run()