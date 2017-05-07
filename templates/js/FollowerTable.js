var FollowerTable = React.createClass({

  getInitialState: function() {
    var organizedResources = JSON.parse('{{ organized_resources }}');
    return {
      organizedResources: organizedResources
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

  _getFollowerComponents: function() {
    var components = [];
    var followers = this._getFollowers();
    var count;
    for (var follower in followers){
      if (followers.hasOwnProperty(follower)) {
        count = followers[follower];
        components.push(
          <FollowerRow
            follower={follower}
            count={count}/>
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
              </tr>
            </thead>
            <tbody>
             { this._getFollowerComponents()}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

});

ReactDOM.render(
  <FollowerTable />,
  document.getElementById('reactContainer')
);
