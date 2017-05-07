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
                  resourceType='resources'
                  className='resource-image-with-count'/>
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
                    resourceType='followers'
                    className='follower-image-with-count'/>
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
      var building = buildings[building_index];
      building.seconds_since_last_tick += 1;
      var organizedResources = prevState.organizedResources;
      if (building.seconds_since_last_tick == building.seconds_between_ticks){
        var data = {'gained_resources': building.production_per_tick_dict};
        this._updateResources(data, organizedResources);
      }
      return {
        buildings: buildings,
        organizedResources: organizedResources
      }
    });
  },

  _updateResources: function(data, organizedResources){
    var resourceType;
    var resourceName;
    var playerResources;
    for (resourceName in data['used_resources']){
      if (data['used_resources'].hasOwnProperty(resourceName)){
        for (resourceType in organizedResources){
          if (organizedResources.hasOwnProperty(resourceType)){
            playerResources = organizedResources[resourceType];
            if (playerResources.hasOwnProperty(resourceName)){
              playerResources[resourceName] -= respData['used_resources'][resourceName];
            }
          }
        }

      }
    }
    for (resourceName in data['gained_resources']){
      if (data['gained_resources'].hasOwnProperty(resourceName)){
        for (resourceType in organizedResources){
          if (organizedResources.hasOwnProperty(resourceType)){
            playerResources = organizedResources[resourceType];
            if (playerResources.hasOwnProperty(resourceName)){
              playerResources[resourceName] += data['gained_resources'][resourceName];
            }
          }
        }

      }
    }
  },

  _addBuildingAndRemoveResources: function(buildingIndex, respData){
    this.setState(function(prevState) {
      var buildings = prevState.buildings;
      buildings[buildingIndex].count += 1;
      var organizedResources = prevState.organizedResources;
      this._updateResources(respData, organizedResources);
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
          <table className="table">
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
