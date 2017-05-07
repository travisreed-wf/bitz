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
