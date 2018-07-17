
venv/bin/pip3.6 freeze > requirements.txt


To check internal / external links, I reconstruct the full URL and compare against 
the current wikipedia domain, but one could probably assume than any link starting
with http/https is external while relative links are internal because wikipedia links
seem normalized that way.

I assume only links inside a paragraph in the article are valid(inside a <p> tag), and ignore links in floating boxes.

Assuming beautifulsoup descendants respect the document ordering which is currently the case(https://stackoverflow.com/questions/37491970/beautifulsoup-what-order-does-descendants-go-in)

Frontend created using https://github.com/facebook/create-react-app => npx create-react-app my-app
