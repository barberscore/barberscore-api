import Ember from 'ember';

export default Ember.Controller.extend({
  appearancesSortProperties: [
    'num',
  ],
  sortedAppearances: Ember.computed.sort(
    'model.appearances',
    'appearancesSortProperties'
  ),
});
