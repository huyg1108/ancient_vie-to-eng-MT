from requests_html import HTMLSession

# Start a session
session = HTMLSession()

# Request the page and render JavaScript
i = 0
total_sentences = 0
while True:
    i += 1
    link = "https://www.nomfoundation.org/nom-project/Ho-Xuan-Huong/Ho-Xuan-Huong-of-poems/" + str(i)
    response = session.get(link)
    response.html.render(timeout=20)  # Render JavaScript (set timeout as needed)
    if response.status_code == 200:
        print("Success")
    # Access page content   
    # Optionally, find specific elements
    elements = response.html.find('td.alt2')  # Replace with actual class name
    total_sentences += len(elements[0].text.split('\n'))
    print(i)
    print(len(elements[0].text.split('\n')))
    print(total_sentences)
    print(elements[0].text.split('\n'))
