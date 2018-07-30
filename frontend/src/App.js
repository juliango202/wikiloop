import React from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import AutorenewIcon from "@material-ui/icons/Autorenew";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import WikipediaCard from "./WikipediaCard.js";

const WIKIPEDIA_URL_MSG =
  "Please enter a valid Wikipedia URL, e.g. https://en.wikipedia.org/wiki/Water";

const styles = theme => ({
  root: {
    flexGrow: 1
  },
  results: {
    margin: 10
  },
  card: {
    minWidth: 275,
    margin: 10
  },
  title: {
    fontSize: 14
  },
  button: {
    margin: theme.spacing.unit,
    marginTop: 30
  },
  buttonIcon: {
    marginLeft: theme.spacing.unit
  }
});

const GameStates = Object.freeze({
  START: Symbol("start"),
  WAITING: Symbol("waiting"),
  RESULTS: Symbol("results")
});

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      startUrl: "https://en.wikipedia.org/wiki/Watermelon",
      startUrlError: "",
      stopUrl: "https://en.wikipedia.org/wiki/philosophy",
      stopUrlError: "",
      gameState: GameStates.START,
      wikiloop: {}
    };
  }

  handleUrlChange = event => {
    const url = event.target.value.toLowerCase();
    if (!url) {
      this.setState({
        [event.target.name]: "",
        [event.target.name + "Error"]: ""
      });
      return;
    }

    // Validate URL format
    const isValidUrl = url.match(/^https?:\/\/\w\w\.wikipedia\.org\/wiki\/\w+/);

    this.setState({
      [event.target.name + "Error"]: isValidUrl ? "" : WIKIPEDIA_URL_MSG,
      [event.target.name]: url
    });
  };

  handleButtonClick = event => {
    // Call backend API to compute journey
    fetch("/api/wikiloop", {
      method: "post",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: JSON.stringify({
        start_url: this.state.startUrl,
        stop_url: this.state.stopUrl
      })
    })
      .then(response => {
        return response.json();
      })
      .then(json => {
        this.setState({
          wikiloop: json,
          gameState: GameStates.RESULTS
        });
      })
      .catch(error => {
        this.setState({
          wikiloop: { error: error.toString() },
          gameState: GameStates.RESULTS
        });
      });
    this.setState({ gameState: GameStates.WAITING });
  };

  render() {
    const { classes } = this.props;
    const state = this.state;
    const { wikiloop, gameState } = state;
    const isValidJourney =
      state.startUrl &&
      state.stopUrl &&
      !state.startUrlError &&
      !state.stopUrlError;

    return (
      <div className={classes.root}>
        <AppBar position="static" color="default">
          <Toolbar>
            <Typography variant="title" color="inherit">
              Wikiloop: A Wikipedia exploration game
            </Typography>
          </Toolbar>
        </AppBar>

        <Card className={classes.card}>
          <CardContent>
            <Typography className={classes.title} color="textSecondary">
              Define your journey
            </Typography>
            <TextField
              error={Boolean(this.state.startUrlError)}
              id="start"
              label={this.state.startUrlError || "Wikipedia starting page"}
              margin="normal"
              name="startUrl"
              value={this.state.startUrl}
              onChange={this.handleUrlChange}
              fullWidth
            />
            <TextField
              error={Boolean(this.state.stopUrlError)}
              id="stop"
              label={this.state.stopUrlError || "Wikipedia goal page"}
              margin="normal"
              name="stopUrl"
              value={this.state.stopUrl}
              onChange={this.handleUrlChange}
              fullWidth
            />

            <Grid container justify="center">
              <Button
                onClick={this.handleButtonClick}
                variant="extendedFab"
                color="primary"
                className={classes.button}
                disabled={!isValidJourney || gameState === GameStates.WAITING}
              >
                Compute path
                <AutorenewIcon className={classes.buttonIcon} />
              </Button>
            </Grid>
          </CardContent>
        </Card>

        {gameState !== GameStates.START && (
          <Card className={classes.card}>
            <CardContent>
              {gameState === GameStates.WAITING && (
                <Typography className={classes.title} color="textSecondary">
                  Looking for a path, please wait...
                </Typography>
              )}

              {gameState === GameStates.RESULTS &&
                wikiloop.error && (
                  <Typography className={classes.title} color="error">
                    {wikiloop.error}
                  </Typography>
                )}

              {gameState === GameStates.RESULTS &&
                !wikiloop.error && (
                  <Typography className={classes.title} color="textPrimary">
                    There is a path! ( ￣▽￣)/
                  </Typography>
                )}
            </CardContent>
          </Card>
        )}

        {gameState === GameStates.RESULTS &&
          wikiloop.journey && (
            <Grid container className={classes.results}>
              <Grid item>
                <Grid container justify="center" spacing={Number(16)}>
                  {wikiloop.journey.map(item => (
                    <Grid item key={item.title}>
                      <WikipediaCard {...item} />
                    </Grid>
                  ))}
                </Grid>
              </Grid>
            </Grid>
          )}
      </div>
    );
  }
}

App.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(App);
