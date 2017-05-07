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
        <div className={"progress-bar progress-bar-striped active" + this._getExtraClass()} role="progressbar" aria-valuenow={this._getStrWidth()}
          aria-valuemin="0" aria-valuemax="100" style={ {width: this._getStrWidth() + "%" } }>
          {this._getLeftText()} / {this.props.rightNumber}
        </div>
      </div>
    )
  }

});
