var BuildingTable = React.createClass({

  getInitialState: function() {

    var buildings = JSON.parse('{{ serialized_buildings }}');
    var playerResources = JSON.parse('{{ serialized_player_resources }}');
    console.log(buildings);
    return {
      buildings: buildings,
      playerResources: playerResources
    };
  },

  _getBuildingComponents: function() {
    var components = [];
    for (var i=0; i< this.state.buildings.length; i++){
      components.push(
        <BuildingRow
          building={this.state.buildings[i]}
          playerResources={this.state.playerResources}
          newBuildingClickHandler={this.handleNewBuildingClick}
          tickHandler={this.tickHandler}
          buildingIndex={i}/>
      )
    }
    return components;
  },

  tickHandler: function(building_index) {
    this.setState(function(prevState) {
      var buildings = prevState.buildings;
      buildings[building_index].seconds_since_last_tick += 1;
      return {
        buildings: buildings
      }
    });
  },

  _addBuildingAndRemoveResources: function(buildingIndex, respData){
    this.setState(function(prevState) {
      var resourceName;
      var buildings = prevState.buildings;
      buildings[buildingIndex].count += 1;
      var playerResources = prevState.playerResources;
      for (resourceName in respData['used_resources']){
        if (respData['used_resources'].hasOwnProperty(resourceName)){
          if (playerResources.hasOwnProperty(resourceName)){
            playerResources[resourceName] -= respData['used_resources'][resourceName];
          }
        }
      }

      return {
        buildings: buildings,
        playerResources: playerResources
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
        console.log('attempting update');
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
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Production per tick</th>
            <th>Progress toward tick</th>
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
    );
  }

});

ReactDOM.render(
  <BuildingTable />,
  document.getElementById('reactContainer')
);
