var ProgressBarComponent = React.createClass({

  getWidth: function() {
    if (this.props.rightNumber == 0){
      return 100
    }
    var width = (100 * this.props.leftNumber / this.props.rightNumber);
    if (this.props.wrapAutomatically) {
      return width % 100
    }
    else if (width > 100){
      return 100;
    }
    else {
      return width;
    }

  },

  _getStrWidth: function() {
    return this.getWidth().toString();
  },

  _getExtraClass: function() {
    if (this.props.leftNumber >= this.props.rightNumber){
      return this.props.extraClassWhenFull
    }
    return '';
  },

  _getLeftText: function() {
    if (this.props.rightNumber == 0){
      return this.props.leftNumber;
    }
    if (this.props.wrapAutomatically) {
      return this.props.leftNumber % this.props.rightNumber;
    }
    else {
      return this.props.leftNumber;
    }

  },

  render: function() {
    return (
      <div className="progress">
        <div className={"progress-bar " + this._getExtraClass()} role="progressbar" aria-valuenow={this._getStrWidth()}
          aria-valuemin="0" aria-valuemax="100" style={ {width: this._getStrWidth() + "%" } }>
          {this._getLeftText()} / {this.props.rightNumber}
        </div>
      </div>
    )
  }

});

var ResourceImageWithCount = React.createClass({


  render: function() {
    return (
      <span>
        <img className="resource-image-with-count" src={"/static/img/resources/" + this.props.resource_name + ".png"} />
        <span>{this.props.separator} {this.props.count}</span>
      </span>
    )
  }

});

var BuildingRow = React.createClass({

  getInitialState: function() {
    return {
      seconds_since_last_tick: this.props.building.seconds_since_last_tick,
      seconds_between_ticks: this.props.building.seconds_between_ticks,
      production_per_tick_dict: this.props.building.production_per_tick_dict,
      ticks_per_day: this.props.building.ticks_per_day,
      discounted_cost: this.props.building.discounted_cost,
      undiscounted_cost: this.props.building.undiscounted_cost,
      total_designated_space: this.props.building.total_designated_space || 0,
      count: this.props.building.count,
      size_per_building: this.props.building.size_per_building
    }
  },

  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      1000
    );
  },

  componentWillUnmount() {
    clearInterval(this.timerID);
  },

  tick: function() {
    console.log('ticking');
    this.setState(function(prevState) {
      return {
        seconds_since_last_tick: prevState.seconds_since_last_tick + 1
      };
    });
  },

  handleNewBuildingClick() {
    var _this = this;
    var data = {
      'building': this.props.building.name,
      'count': 1
    };
    $.ajax({
      url: '/build/buildings/',
      method: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      success: function(resp) {
        console.log('attempting update');
        _this.setState(function(prevState) {
          return {
            count: prevState.count + 1
          };
        });
        //update_resources($.parseJSON(resp));
      },
      error: function(resp) {
        window.alert(resp.responseText || 'Unknown Error');
      }
    });

  },

  _getTotalSpaceInUse: function(){
    return this.state.size_per_building * this.state.count;
  },

  _getProductionPerTickComponents: function(){
    var components = [];
    var count;
    for (var resource in this.state.production_per_tick_dict){
      if (this.state.production_per_tick_dict.hasOwnProperty(resource)){
        count = this.state.production_per_tick_dict[resource];
      }
      components.push(
        <ResourceImageWithCount
          resource_name={resource}
          count={count}
          separator=' x'/>
      )
    }
    return components;
  },

  _calculateCostAvailable: function() {
    var availableCount = 0;
    var costToUse = this._determineCostToUse();
    var count;
    for (var resource in costToUse){
      if (costToUse.hasOwnProperty(resource)){
        count = costToUse[resource];
        if (this.props.playerResources.hasOwnProperty(resource)){
          var playerCount = this.props.playerResources[resource];
          if (playerCount > 0){
            if (playerCount > count){
              availableCount += count;
            }
            else {
              availableCount += playerCount;
            }
          }
        }
      }
    }
    return availableCount

  },

  _determineCostToUse: function(){
    if (this.state.total_designated_space > this._getTotalSpaceInUse()){
      return this.state.discounted_cost;
    }
    else {
      return this.state.undiscounted_cost;
    }
  },

  _calculateTotalCost: function() {
    var costToUse = this._determineCostToUse();
    var totalCostCount = 0;

    for (var resource in costToUse) {
      if (costToUse.hasOwnProperty(resource)) {
        var count = costToUse[resource];

        if (count <= 0) {
          continue;
        }

        totalCostCount += count;
      }
    }
    return totalCostCount;
  },

  _getProductionPerDayComponents: function(){
    var components = [];
    var count;
    for (var resource in this.state.production_per_tick_dict){
      if (this.state.production_per_tick_dict.hasOwnProperty(resource)){
        count = this.state.production_per_tick_dict[resource] * this.state.ticks_per_day;
      }
      components.push(
        <ResourceImageWithCount
          resource_name={resource}
          count={count}
          separator=' x'/>
      )
    }
    return components;
  },

  _getActionDiv: function(){
    if (this._calculateCostAvailable() >= this._calculateTotalCost()){
      return <button className="btn btn-success" type='button' style={ {width: "100%"} } data-toggle='tooltip' onClick={this.handleNewBuildingClick}>Build { this.props.building.name }</button>;
    }
    else {
      return (
        <ProgressBarComponent
          leftNumber={ this._calculateCostAvailable()}
          rightNumber={ this._calculateTotalCost()}
          wrapAutomatically={false}/>
      )
    }
  },


  _getCostComponents: function(){
    var components = [];
    var count;
    var cost_to_use;
    var asterisk;
    if (this.state.total_designated_space > this._getTotalSpaceInUse()){
      cost_to_use = this.state.discounted_cost;
    }
    else {
      asterisk = <span className='extra-cost-asterisk' data-toggle="tooltip" title="Cost increased because no suitable tiles are assigned to this building">*</span>;
      cost_to_use = this.state.undiscounted_cost;
    }
    for (var resource in cost_to_use){
      if (cost_to_use.hasOwnProperty(resource)){
        count = cost_to_use[resource]
      }
      components.push(
        <span>
          <ResourceImageWithCount
            resource_name={resource}
            count={count}
            separator=' x'/>
          {asterisk}
        </span>
      )
    }
    return components;
  },
  render: function() {

    return (
      <tr>
        <td style={ {verticalAlign:'middle'} }>
          <img className='building-resource-image' src={"/static/img/resources/" + this.props.building.name + ".png"} /> <span>{this.props.building.name}</span>
        </td>
        <td style={ {verticalAlign:'middle'} }>
          { this._getProductionPerTickComponents()}
        </td>
        <td style={ {verticalAlign:'middle'} }>
          <ProgressBarComponent
            leftNumber={this.state.seconds_since_last_tick}
            rightNumber={this.state.seconds_between_ticks}
            wrapAutomatically={true}/>
        </td>
        <td style={ {verticalAlign:'middle'} }>
          { this._getProductionPerDayComponents()}
        </td>
        <td style={ {verticalAlign:'middle'} }>
          { this._getCostComponents() }
        </td>
        <td style={ {verticalAlign:'middle'} }>
          <span>{this.state.count}</span>
        </td>
        <td style={ {verticalAlign:'middle'} }>
          <ProgressBarComponent
          leftNumber={this._getTotalSpaceInUse()}
          rightNumber={this.state.total_designated_space}
          extraClassWhenFull='progress-bar-danger'
          wrapAutomatically={false} />
        </td>
        <td style={ {verticalAlign:'middle'} }>
          { this._getActionDiv() }
        </td>
      </tr>
    );
  }

});
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
          playerResources={this.state.playerResources}/>
      )
    }
    return components;
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
