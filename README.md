## Notes

- To check internal / external links, I reconstruct the full URL and compare against
  the current wikipedia domain, but one could probably assume than any link starting
  with http/https is external while relative links are internal because wikipedia links
  seem normalized that way.

- I assume only links inside a paragraph in the article are valid(inside a &lt;p&gt; tag), and ignore links in floating boxes.

- Frontend created using material-ui & https://github.com/facebook/create-react-app => npx create-react-app my-app

## Extra Optional features

- Provide a way to change the target page => Done

## Next steps for prod deployment

- Add a rate limiting system to our requests to wikipedia. Also the information on wikipedia pages should be cached for some duration, possibly in a local database.
- Add some tests
- Use env variable for API url to be able to change it dynamically
- Docker PROD config => I have very little experience in Docker so I don't know

## Version 2.0 features

- Use WebSockets to stream the visited pages back to the client and see the path in real-time
- Better UX
