
To check internal / external links, I reconstruct the full URL and compare against
the current wikipedia domain, but one could probably assume than any link starting
with http/https is external while relative links are internal because wikipedia links
seem normalized that way.

I assume only links inside a paragraph in the article are valid(inside a &lt;p&gt; tag), and ignore links in floating boxes.

Frontend created using https://github.com/facebook/create-react-app => npx create-react-app my-app

Improvements:
* Use WebSockets to stream the visited pages back to the client and see the path in realtime