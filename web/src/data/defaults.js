const WireActionsBase = [
  { text: 'Bank Transfer', value: 'bank_transfer' },
  { text: 'Convert', value: 'convert' },
  { text: 'CONTRA', value: 'contra' },
];

export const WireActionsForDisplay = [
  { text: 'Multiple', value: 'multiple' },
  ...WireActionsBase,
];

export const WireActionsFilters = [
  { text: 'All', value: null },
  { text: '-', value: 'unspecified' },
  ...WireActionsForDisplay,
];

export const WireActions = [
  {
    value: null,
    text: '–',
  },
  ...WireActionsBase,
];

export const WireStatusesFilters = [
  { text: 'All', value: null },
  { text: 'Confirmed', value: 'confirmed' },
  { text: 'Unconfirmed', value: 'unconfirmed' },
];

export const MappedWireActions = WireActionsForDisplay.reduce(
  (map, wireAction) => ({
    ...map,
    [wireAction.value]: wireAction.text,
  }),
  {}
);
