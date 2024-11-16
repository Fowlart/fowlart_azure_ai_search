from src.utils.common_utils import  analyze_text

if __name__ == "__main__":

    #analyze_text("""I've read the author of "War of THE worlds": cool stuff""", "en.lucene","fowlart_product_review_hybrid")

    #analyze_text("""I've read the author of "War of THE worlds": cool stuff""","en.microsoft","fowlart_product_review_hybrid")

    analyze_text(r"Dog+cat>pig are!=n=", "my_custom_analyzer", "fowlart_product_review_hybrid")

    # analyze_text(text="""
    # Це є демонстрація мовного аналізу українського тексту!
    # Я хочу їсти яблука з цукром!""",
    #              analyzer_name="uk.microsoft",
    #              index_name="fowlart_product_review_hybrid")
