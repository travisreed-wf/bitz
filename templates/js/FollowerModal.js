var FollowerModal = React.createClass({

  _getSelect: function(){
    var action = this.props.selectedAction;
    console.log('action ');
    console.log(action);
    if (action && action.hasOwnProperty('info_needed') && Object.keys(action['info_needed']).length != 0) {
      var options = [];
      var infoNeeded = action['info_needed'];
      if (infoNeeded && infoNeeded.hasOwnProperty('options')) {
        var actionOptions = infoNeeded['options'];
      }
      else {
        actionOptions = [];
      }
      for (var i = 0; i < actionOptions.length; i++) {
        var actionOption = actionOptions[i];
        var option = <option value={actionOption}>{actionOption}</option>;
        options.push(option);
      }
      return (
        <select className="form-control" id="option">
          {options}
        </select>
      )
    }
    return <div></div>

  },

  _selectedActionName: function(){
    if (this.props.selectedAction && this.props.selectedAction['info_needed']){
      return this.props.selectedAction['info_needed']['name'];
    }
    else{
      return '';
    }
  },

  render: function() {

    return (
      <div className="modal fade" id="followerModal">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
              <h4 className="modal-title">Perform Follower Action - {this.props.selectedAction['name']}</h4>
            </div>
            <div className="modal-body">
              <label for="option">{this._selectedActionName()}</label>
              {this._getSelect()}
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
              <button type="button" className="btn btn-primary" onClick={() => this.props.modalClickHandler()}>Save changes</button>
            </div>
          </div>
        </div>
      </div>
    )
  }
});
