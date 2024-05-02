import React from 'react';
import { ConfigProvider } from 'antd';

const whiteOne = '#d8d8d8';

const StyleProvider = (props: { children?: React.ReactNode }) => {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: whiteOne,
        },
        components: {
          Checkbox: {
            colorBgContainer: whiteOne,
            algorithm: true,
          },
        },
      }}
    >
      {props.children}
    </ConfigProvider>
  );
};

export default StyleProvider;
