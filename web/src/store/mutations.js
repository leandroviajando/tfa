export default {
  initialiseStore(state) {
    const selColsStored = localStorage.getItem('selectedColumns');
    const drafts = localStorage.getItem('drafts');
    if (selColsStored) {
      state.selectedColumns = JSON.parse(selColsStored);
    }
    if (drafts) {
      state.drafts = JSON.parse(drafts);
    } else {
      state.drafts = {};
    }
  },

  TOGGLE_NAVBAR(state, isMdAndDown) {
    state.navBar.minify = isMdAndDown ? false : !state.navBar.minify;
    state.navBar.show = isMdAndDown ? !state.navBar.show : true;
  },
  SET_USER(state, user) {
    state.user = user;
  },
  SET_BALANCES(state, value) {
    state.balances = value;
  },
};
