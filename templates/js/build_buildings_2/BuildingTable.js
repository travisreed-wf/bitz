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
    var components = [];
    var resourceTypes = ['basic', 'earned'];
    var resources = [];
    var resourceType;
    var resource;
    var count;
    for (var i=0; i<resourceTypes.length; i++){
      resourceType = resourceTypes[i];
      if (this.state.organizedResources.hasOwnProperty(resourceType)){
        resources = this.state.organizedResources[resourceType];
        components.push(<h5>{resourceType}</h5>);
        for (resource in resources){
          if (resources.hasOwnProperty(resource)){
            count = resources[resource];
            components.push(
              <div>
                <SpanCountComponentWithName
                  count={count}
                  resource={resource}
                  resourceType='resources'/>
              </div>);
          }
        }
      }
    }
    resourceTypes = ['follower'];
    for (var i=0; i<resourceTypes.length; i++){
      resourceType = resourceTypes[i];
      if (this.state.organizedResources.hasOwnProperty(resourceType)){
        resources = this.state.organizedResources[resourceType];
        components.push(<h5>{resourceType}</h5>);
        for (resource in resources){
          if (resources.hasOwnProperty(resource)){
            count = resources[resource];
            if (count > 0){
              components.push(
                <div>
                  <SpanCountComponentWithName
                    count={count}
                    resource={resource}
                    resourceType='followers'/>
                </div>);
            }
          }
        }
      }
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
      var organizedResources = prevState.organizedResources;
        var resourceType;
      for (resourceName in respData['used_resources']){
        if (respData['used_resources'].hasOwnProperty(resourceName)){
          for (resourceType in organizedResources){
            if (organizedResources.hasOwnProperty(resourceType)){
              var playerResources = organizedResources[resourceType];
              if (playerResources.hasOwnProperty(resourceName)){
                playerResources[resourceName] -= respData['used_resources'][resourceName];
              }
            }
          }

        }
      }

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
      <div>
        <div className="col-md-2 col-sm-2">
          <h4>Resources</h4>
          { this._getResourceComponents() }
        </div>
        <div className="col-md-9 col-sm-9">
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
        </div>
      </div>
    );
  }

});

ReactDOM.render(
  <BuildingTable />,
  document.getElementById('reactContainer')
);
