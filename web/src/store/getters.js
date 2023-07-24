export default {
  user: (state) => {
    return state.user;
  },
  balances: (state) => state.balances,
  navbarMinified: (state) => state.navBar.minify,
  navbarShow: (state) => state.navBar.show,
};
