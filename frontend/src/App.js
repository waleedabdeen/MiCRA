import React from 'react';
import './App.css';
import { ConfigProvider, Image, Layout, Menu } from 'antd';
import { Content, Header } from 'antd/es/layout/layout';
import menuItem from './menuItems';
import TracingPage from './pages/TracingPage/TracingPage';
import LabeledDataPage from './pages/LabeledDataPage/LabeledDataPage';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

function App() {
  const router = createBrowserRouter([
    {
      path: '/',
      element: <TracingPage />
    },
    {
      path: 'labeled-data',
      element: <LabeledDataPage />
    }
  ]);

  const navigate = (destination) => {

  };

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#434343'
        },
      }}
    >
      <Layout>
        <Header className='header'>
          <Image height={60} src='bth_white_logo_small.png' />
          <h2 className="website-title">
            Taxonomic Trace Links: an ML Supported Traceability
          </h2>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['2']}
            items={menuItem}
            onClick={({ key }) => navigate(key)}
          />
        </Header>
        <Content className='content'>
          <RouterProvider router={router} />
          {/* <TracingPage /> */}
        </Content>
      </Layout>

    </ConfigProvider >
  );
}

export default App;
