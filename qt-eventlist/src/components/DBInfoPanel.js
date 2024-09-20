import React, { useState, useEffect } from 'react';

function DBInfoPanel(props){

	const titles =['ファイル', 'アップロード日時', 'データ数', '先頭', '最終','ステータス'];

	const [dbi, setDBInfo] = useState(null);
	const [upli, setULInfo] = useState([]);
	const [tableChanged, setTableChanged] = useState(false);
	const [haveData, setHaveData] = useState(false);
	const setChanged = props.setChanged;
	
	
	useEffect(() => {
		fetch('http://127.0.0.1:8000/api/Activity/activity_db_info/1/')
		.then(response => {
			return response.json();
		})
		.then(result =>{
			const txt = JSON.stringify(result, null,' ');
			console.log('---Success ---');
			console.log(txt);
			let res = JSON.parse(txt);
			setDBInfo(res);
			
		})
		.catch(error =>{
			console.error('----Error---');
			console.error(error);
		})
		
		fetch('http://127.0.0.1:8000/api/Activity/file_upload/')
		.then(response => {
			return response.json();
		})
		.then(result =>{
			const txt = JSON.stringify(result, null,' ');
			console.log('---Success ---');
			console.log(txt);
			let res = JSON.parse(txt);
			setULInfo(res);
			setHaveData(true);
		})
		.catch(error =>{
			console.error('----Error---');
			console.error(error);
		})
		
		setChanged(false);
		setTableChanged(false);
				
	},[props, tableChanged]);
	
	if(haveData){
	return(
		<div className="db_info_panel">
			<div className="db_status">
				<label>アクティビティーデータ情報</label>
					<table className="db_table">
						<tr><td>先頭データ</td><td>{dbi['startTime']}</td></tr>
						<tr><td>最終データ</td><td>{dbi['endTime']}</td></tr>
						<tr><td>データ数</td><td>{dbi['count']}</td></tr>
					</table>
			</div>
			<div className="upload_info">
				<label>ファイルアップロード情報</label>
				<table className="db_table">
					<tr>
						{titles.map((title) => {
							return <th>{title}</th>;
						})}
					</tr>
					{upli.map((ui) =>{
						return(
							<tr>
								<td> {ui['fileName']}</td>
								<td> {ui['uploadTime']}</td>
								<td> {ui['dataCount']}</td>
								<td> {ui['startTime']}</td>
								<td> {ui['endTime']}</td>
								<td> {ui['status']}</td>
							</tr>
						)
					})}
				
				</table>
			</div>
		</div>
	)
}

}

export default DBInfoPanel;