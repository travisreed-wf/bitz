var FollowerTable = React.createClass({

  getInitialState: function() {
    var organizedResources = JSON.parse('{{ organized_resources }}');
    var followerData = JSON.parse('{{ follower_data }}');

    return {
      organizedResources: organizedResources,
      followerData: followerData,
      selectedAction: {}
    };
  },

  _getResourceComponents: function() {
    return getResourceComponent(this.state.organizedResources);
  },

  _getFollowers: function() {
    if (this.state.organizedResources.hasOwnProperty(['follower'])){
      return this.state.organizedResources['follower']
    }
    return []
  },

  _getFollowerData: function(followerName){
    if (this.state.followerData.hasOwnProperty(followerName)){
      return this.state.followerData[followerName];
    }
    return {};
  },

  _clickHandler: function(actionIndex, followerName){
    console.log(actionIndex);
    console.log(followerName);
    var action = this._getFollowerData(followerName)['actions'][actionIndex];
    var modal = $('#followerModal');
    this.setState({selectedAction: action});
    modal.modal("show");
  },

  _getFollowerComponents: function() {
    var components = [];
    var followers = this._getFollowers()
    var count;
    for (var follower in followers){
      if (followers.hasOwnProperty(follower)) {
        count = followers[follower];
        components.push(
          <FollowerRow
            follower={follower}
            count={count}
            data={this._getFollowerData(follower)}
            actionHandler={this._clickHandler}/>
        )
      }
    }
    return components;
  },

  render: function() {
    return (
      <div>
        <div className="col-md-2 col-sm-2">
          <h4>Resources</h4>
          { this._getResourceComponents() }
        </div>
        <div className="col-md-9 col-sm-9">
          <table className="table table-responsive">
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Count</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
             { this._getFollowerComponents()}
            </tbody>
          </table>
        </div>
        <FollowerModal
          selectedAction={this.state.selectedAction} />
      </div>
    );
  }

});

ReactDOM.render(
  <FollowerTable />,
  document.getElementById('reactContainer')
);
