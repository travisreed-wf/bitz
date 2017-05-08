var ResourceImageWithCount = React.createClass({

  _getDataToggle: function(){
    if (this.props.tooltip){
      return 'tooltip';
    }
    return '';

  },

  render: function() {
    return (
      <span title={this.props.tooltip} data-toggle={this._getDataToggle()}>
        <img className="resource-image-with-count" src={"/static/img/resources/" + this.props.resource_name + ".png"} />
        <span>{this.props.separator} {this.props.count}</span>
      </span>
    )
  }

});
