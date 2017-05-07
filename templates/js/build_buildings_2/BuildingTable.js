var BuildingTable = React.createClass({

  getInitialState: function() {
    var buildings = JSON.parse('{{ serialized_buildings }}');
    var organizedResources = JSON.parse('{{ organized_resources }}');
    return {
      buildings: buildings,
      organizedResources: organizedResources
    };
  },

  _getBuildingComponents: function() {
    var components = [];
    for (var i=0; i< this.state.buildings.length; i++){
      components.push(
        <BuildingRow
          building={this.state.buildings[i]}
          organizedResources={this.state.organizedResources}
          newBuildingClickHandler={this.handleNewBuildingClick}
          tickHandler={this.tickHandler}
          buildingIndex={i}/>
      )
    }
    return components;
  },

  _getResourceComponents: function() {
    return getResourceComponent(this.state.organizedResources);
  },

  tickHandler: function(building_index) {
    this.setState(function(prevState) {
      var buildings = prevState.buildings;
      var building = buildings[building_index];
      building.seconds_since_last_tick += 1;
      var organizedResources = prevState.organizedResources;
      if (building.seconds_since_last_tick == building.seconds_between_ticks){
        var data = {'gained_resources': building.production_per_tick_dict};
        updateResources(data, organizedResources);
      }
      return {
        buildings: buildings,
        organizedResources: organizedResources
      }
    });
  },

  _addBuildingAndRemoveResources: function(buildingIndex, respData){
    this.setState(function(prevState) {
      var buildings = prevState.buildings;
      buildings[buildingIndex].count += 1;
      var organizedResources = prevState.organizedResources;
      updateResources(respData, organizedResources);
      return {
        buildings: buildings,
        organizedResources: organizedResources
      }
    });
  },

  handleNewBuildingClick(buildingIndex) {
    var _this = this;
    var building = this.state.buildings[buildingIndex];
    var data = {
      'building': building.name,
      'count': 1
    };
    $.ajax({
      url: '/build/buildings/',
      method: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      success: function(resp) {
        _this._addBuildingAndRemoveResources(buildingIndex, JSON.parse(resp));
        //update_resources($.parseJSON(resp));
      },
      error: function(resp) {
        window.alert(resp.responseText || 'Unknown Error');
      }
    });

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
                <th>Production per tick</th>
                <th>Progress toward tick (s)</th>
                <th>Production per day</th>
                <th>Cost</th>
                <th>Count</th>
                <th>Used Space</th>
                <th>Build</th>
              </tr>
            </thead>
            <tbody>
             { this._getBuildingComponents()}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

});

ReactDOM.render(
  <BuildingTable />,
  document.getElementById('reactContainer')
);
