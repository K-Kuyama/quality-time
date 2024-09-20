import React, { useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

import 'bootstrap/dist/css/bootstrap.min.css';

import ActivityListPage from "../pages/ActivityListPage";
import AllGraphsPage from "../pages/AllGraphsPage";

function NavigationMenu(props){

	return(
		<Navbar expand="lg" className="bg-body-tertiary"  data-bs-theme="dark">
                <Container>
                    <Navbar.Brand href="#home">QT</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="mr-auto">
                            <Nav.Link href="#db">ダッシュボード</Nav.Link>
                            <Nav.Link href="/">アクティビティリスト</Nav.Link>                                
                            <NavDropdown title="集計表示" id="basic-nav-dropdown">
                                <NavDropdown.Item href="/date_graphs"> 日次集計情報 </NavDropdown.Item>
                                <NavDropdown.Item href="/week_graphs"> 週次集計情報 </NavDropdown.Item>
                                <NavDropdown.Item href="/month_graphs"> 月次集計情報 </NavDropdown.Item>
                                <NavDropdown.Item href="/year_graphs"> 年次集計情報 </NavDropdown.Item>
                                <NavDropdown.Divider />
                                <NavDropdown.Item href="/bar_graphs"> 総合集計情報(P) </NavDropdown.Item>
                                <NavDropdown.Item href="/all_graphs"> 総合集計情報 </NavDropdown.Item>
                            </NavDropdown>
                            <NavDropdown title="分類表示" id="category-nav-dropdown">
                                <NavDropdown.Item href="/categorize"> 分類表示 </NavDropdown.Item>
                                <NavDropdown.Item href="/multi_categorize"> 複合分類表示 </NavDropdown.Item>                                
                            </NavDropdown>
                            <Nav.Link href="/editor">分類条件の設定</Nav.Link>   
                            <Nav.Link href="/data_and_files">データアップロード</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
           </Navbar>	
	);

}

export default NavigationMenu;