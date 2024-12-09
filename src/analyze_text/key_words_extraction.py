from src.utils.common_utils import extract_key_phrases, get_text_analytics_client

if __name__=="__main__":

    text_analytics_client = get_text_analytics_client()

    text_us = """
    For 12 years Sophie had been experiencing painful periods, weight gain, depression and fatigue.
    She had been diagnosed with polycystic ovary syndrome (PCOS), a hormonal condition that affects about one 
    in 10 women, but she struggled to get medical help.She felt her only option was to take her health 
    into her own hands, and it was 
    at this moment that Kourtney Simmang came up on her recommended page on Instagram.
    Kourtney promised to treat the “root cause” of PCOS, even though researchers have not yet identified one. 
    She offered customers laboratory tests, a “health protocol”- a diet and supplement plan - and coaching 
    for $3,600 (£2,800). Sophie signed up, paying hundreds of dollars more for supplements through Kourtney’s affiliate links.
    Dr Jen Gunter, a gynaecologist and women’s health educator, said Kourtney wasn’t qualified to order the tests she
     was selling, and that they had limited clinical use.
     After nearly a year Sophie’s symptoms hadn’t improved, so she gave up Kourtney’s cure.
     “I left the programme with a worse relationship to my body and food, 
     [feeling] that I didn’t have the capacity to improve my PCOS,” she said.Kourtney did not respond 
     to requests for comment.Medically unqualified influencers - many with more than a million followers - 
     are exploiting the absence of an easy medical solution for PCOS by posing as experts and selling fake cures.
     Some describe themselves as nutritionists or “hormone coaches”, but these accreditations can be done 
     online in a matter of weeks. The BBC World Service tracked the most-watched videos 
     with a “PCOS” hashtag on TikTok and Instagram during the month of September and found that 
     half of them spread false information.
    """

    text_ukr = """
     Протягом 12 років Софі страждала від хворобливих менструацій, збільшення ваги, депресії та втоми.
     У неї був діагностований синдром полікістозних яєчників (СПКЯ), гормональний стан, який вражає приблизно одну
     у 10 жінок, але їй було важко отримати медичну допомогу. Вона вважала, що її єдиний вихід — це взяти своє здоров’я
     в її власні руки, і це було
     у цей момент Кортні Сімманг зайшла на рекомендовану нею сторінку в Instagram.
     Кортні пообіцяла лікувати «основну причину» СПКЯ, хоча дослідники ще не виявили її.
     Вона пропонувала клієнтам лабораторні тести, «протокол здоров’я» — дієту та план добавок — і інструктаж
     за $3600 (£2800). Софі зареєструвалася, заплативши сотні доларів більше за добавки через партнерські посилання Кортні.
     Доктор Джен Гантер, гінеколог і викладач жіночого здоров’я, сказала, що Кортні не має кваліфікації, щоб замовляти тести, які вона проводить.
     продавався, і що вони мали обмежене клінічне використання.
     Через майже рік симптоми Софі не покращилися, тому вона відмовилася від лікування Кортні.
     «Я залишив програму з гіршим ставленням до свого тіла та їжі,
     [відчуття], що я не маю можливості покращити свій СПКЯ», — сказала вона. Кортні не відповіла.
     на запити про коментарі. Медично некваліфіковані впливові особи - багато з них мають понад мільйон підписників -
     використовують відсутність простого медичного рішення для СПКЯ, видаючи себе за експертів і продаючи підроблені ліки.
     Деякі називають себе дієтологами або «гормональними тренерами», але ці акредитації можна отримати
     онлайн за лічені тижні. Всесвітня служба BBC відстежила відео, які найбільше переглядали
     із хештегом «СПКЯ» в TikTok та Instagram протягом вересня місяця та виявив це
     половина з них поширюють неправдиву інформацію."""

    print(extract_key_phrases(
        text=text_us,
        client=text_analytics_client))

    print(extract_key_phrases(text=text_ukr,client=text_analytics_client, language="uk"))