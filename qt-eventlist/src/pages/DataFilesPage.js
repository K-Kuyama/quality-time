import React, { useState, useEffect } from 'react';
import FileUpload from "../components/FileUpload";
import DBInfoPanel from "../components/DBInfoPanel";

/* アクティビティーリストページ */
function DataFilesPage(){
    const [target_date, setDate] = useState(new Date());
    const [item, setItem] = useState("event_list");

	const [changed, setChanged] = useState(false);


	return(
		<div className="app_page">
			<div className="contents">
				<DBInfoPanel setChanged={setChanged} />
				<hr size="5" width="100%" color="white" ></hr>
				<FileUpload setChanged={setChanged} />    
			</div>
		</div>
	)

}

export default DataFilesPage;