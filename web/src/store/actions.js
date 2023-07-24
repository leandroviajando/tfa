import router from '@/router';
import axios from '@/services/axios';

export default {
  setUser: ({ commit }, user) => {
    commit('SET_USER', user);
  },
  setBalances: ({ commit }, balances) => {
    commit('SET_BALANCES', balances);
  },
  async fetchBalances({ commit }) {
    const resp = await axios.get(`/api/v1/balances`);
    const balances = resp.data.map((b) => ({
      value: b.balance_id,
      text: b.balance_name,
    }));
    await commit('SET_BALANCES', balances);
    return balances;
  },
  handleAPIError: ({ commit }, { response, request }) => {
    let message = {
      type: 'error',
      message: 'messages.errors.unknownError',
      persistent: true,
      action: () => router.go(),
      id: 'unknown-error',
      buttonLabel: 'reload',
    };
    if (response?.status === 0 || request?.status === 0) {
      // network error
      message = {
        ...message,
        message: 'messages.errors.connectionError',
        id: 'network-error',
      };
    }
    if (response?.status === 401) {
      if (router.currentRoute.path === '/signin') {
        return;
      }
      if (response.data?.redirectTo) {
        window.location.reload();
        return;
      }
      router.replace({
        path: '/signin',
        query: { r: router.currentRoute.fullPath },
      });
      return;
    }

    if (response?.status === 500) {
      message = {
        ...message,
        message: 'messages.errors.applicationError',
        id: 'application-error',
      };
    }

    const customEndpointErrors = [
      {
        endpoint: '/v2/wires',
        message: {
          type: 'error',
          message: 'messages.errors.wireUpdateError',
          autoDismiss: true,
        },
      },
      {
        endpoint: '/v1/balance-adjustment',
        message: {
          type: 'error',
          message: 'messages.errors.balanceAdjustmentUpdateError',
          autoDismiss: true,
        },
      },
      {
        endpoint: '/v1/wires-export-packages',
        message: {
          type: 'error',
          message: 'messages.errors.exportFailed',
          autoDismiss: false,
        },
      },
    ];

    function getCustomError(url) {
      if (request.responseURL?.includes(url.endpoint)) {
        message = url.message;
      }
    }
    customEndpointErrors.forEach((e) => getCustomError(e));

    commit('ADD_SYSTEM_MESSAGE', message);
  },
};
