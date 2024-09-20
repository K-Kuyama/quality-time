import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Offcanvas from 'react-bootstrap/Offcanvas';
import SidebarDefEditor from './SidebarDefEditor';

function PerspectivePanel(props){

	const [data, setData]= useState([]);
	const [haveData, setHaveData] = useState(false); 
	const [menueChanged, setMenueChanged] = useState(false);
	const setParam = props.handler;
	const setChanged = props.set_check;
	
	const [show, setShow] = useState(false);
	const handleClose = () => setShow(false);
	const handleShow = () => setShow(true);

	const checkPid = () =>{
		if (!data.some(item => item['id'] == props.get_handler())){
			setParam(0)
		}
	}

	const getInitialPid = (data) =>{
		let pid = 0;
		for(let p of data){
			if(p['categorize_model']==null){
				pid = p['id'];
				break;
			}
		}
		return pid;
	} 
	

	/* propsに変更があった時に呼び出される */
	useEffect(() => {
		fetch('http://127.0.0.1:8000/api/user_def/Perspective/')
		.then(response => {
			return response.json();
		})
		.then(result =>{
			const txt = JSON.stringify(result, null,' ');
			console.log('---Success ---');
			console.log(txt);
			let res = JSON.parse(txt);
			setData(res);
			if(!haveData){
				setParam(getInitialPid(res));
			}
			setHaveData(true);
			setChanged(false);
			setMenueChanged(false);
			
			//checkPid();
		})
		.catch(error =>{
			setHaveData(false);
			setChanged(false);
			setMenueChanged(false);
			console.error('----Error---');
			console.error(error);
		})
	
	},[props, menueChanged]);


	if (!haveData) {
		return <div>Loading...</div>
	} else{
		return(
			<>
				<div className="perspectives">	
					<div className="pp_header">
						<Button type="button" className="btn btn-ppheader" data-bs-toggle="button" size="sm" value="edit" 	onClick={handleShow}>
    						編集
    					</Button>
					</div>
    				<div className="d-grid gap-2">
    					{data.map((obj) =>{
    						if(obj['categorize_model']==null){
    							return(
    								<Button type="button" class="btn btn-light" data-bs-toggle="button" variant="light" size="sm" 
    									value={obj['id']} onClick={(e) => setParam(e.target.value)}>
    									{obj['name']}
    								</Button>
    							)
    						}
    					})}
    					
    					{/* <Button type="button" class="btn btn-secondary"  variant="dark" size="md" 
    						value="0" onClick={(e) => setParam(e.target.value)}>
    							+ 新規追加
    					</Button> */}
    					<hr size="5" color="white" ></hr>
    					{data.map((obj) =>{
    						if(obj['categorize_model'] != null){
    							return(
    								<Button type="button" class="btn btn-light" data-bs-toggle="button" variant="light" size="sm" 
    									value={obj['id']} onClick={(e) => setParam(e.target.value)}>
    									{obj['name']}
    								</Button>
    							)
    						}
    					})}

    					
    				</div>
				</div>
				{/* 編集ボタンを押すと現れるオフキャンパス */}
				<Offcanvas show={show} onHide={handleClose}>
        			<Offcanvas.Header closeButton className="perspective-off-title">
          				<Offcanvas.Title >パースペクティブの編集</Offcanvas.Title>
        			</Offcanvas.Header>
        			<Offcanvas.Body className="perspective-offcanvas">
          				<SidebarDefEditor data={data} handler={setMenueChanged}/>
        			</Offcanvas.Body>
      			</Offcanvas>
			</>
		);
	}


}

export default PerspectivePanel;