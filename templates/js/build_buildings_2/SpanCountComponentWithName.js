var SpanCountComponentWithName = React.createClass({

  getInitialState: function () {

    return {
      backgroundColor: '',
      timeOfLastUpdate: new Date()
    };
  },

  _getStyle: function () {
    if (this.state.backgroundColor){
      console.log(this.state.backgroundColor);
      return {paddingBottom: "5px", backgroundColor:this.state.backgroundColor};
    }
    else {
      return {paddingBottom: "5px"};
    }
  },

  render: function(){
    return (
      <span style={this._getStyle()}>
        <img src={"/static/img/" + this.props.resourceType + '/' + this.props.resource + ".png"} className={this.props.className} />  { this.props.resource }: <span>{ this.props.count }</span>
      </span>
    )
  },

  componentDidUpdate(prevProps, prevState){
    var _this = this;
    if (prevProps.count < this.props.count && (new Date() - _this.state.timeOfLastUpdate > 1000)){
      _this.setState({
        backgroundColor: '#5cb85c',
        timeOfLastUpdate: new Date()
      })
    }
    else if (prevProps.count > this.props.count && (new Date() - _this.state.timeOfLastUpdate > 1000)){
      _this.setState({
        backgroundColor: '#d9534f',
        timeOfLastUpdate: new Date()
      })
    }
    else if (this.state.backgroundColor != '' && (new Date() - _this.state.timeOfLastUpdate > 1000)) {
      _this.setState({
        backgroundColor: '',
        timeOfLastUpdate: new Date()
      })
    }
  }
});
