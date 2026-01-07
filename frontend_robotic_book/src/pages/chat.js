import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Chatbot from '@site/src/components/Chatbot/Chatbot';

import Heading from '@theme/Heading';
import styles from './chat.module.css';

function ChatPageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx("hero hero--primary", styles.chatBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          AI Chat Assistant
        </Heading>
        <p className="hero__subtitle">Ask questions about Physical AI & Humanoid Robotics</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro"
          >
            Learn More About the Book
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function ChatPage() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`AI Assistant | ${siteConfig.title}`}
      description="Interactive AI chat for Physical AI & Humanoid Robotics book">
      <ChatPageHeader />
      <main className={styles.chatMain}>
        <div className="container">
          <div className="row">
            <div className="col col--12">
              <div className={styles.chatContainer}>
                <Chatbot />
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}