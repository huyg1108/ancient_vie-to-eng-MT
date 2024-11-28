from requests_html import HTMLSession
import csv
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
    output_file = f"extracted/{i}.csv"
    print(output_file)
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # write elements[0] to eng column and elements[1] to vie column
        vie_sentences = elements[1].text.split('\n')
        eng_sentences = elements[0].text.split('\n')
        csvwriter.writerow(['vie', 'eng'])
        data = list(zip(vie_sentences, eng_sentences))
        csvwriter.writerows(data)
    
        