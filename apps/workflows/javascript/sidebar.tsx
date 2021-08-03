import React from 'react'
import { INode } from './interfaces'

import './styles/_dnd-sidebar.scss'

const NODES = JSON.parse(document.getElementById('nodes').textContent) as INode

const SECTIONS = Object.keys(NODES).reduce((sections, key) => {
  const node = NODES[key]
  const section = node.section

  if (!sections[section]) {
    sections[section] = [key]
  } else {
    sections[section] = [...sections[section], key]
  }

  return sections
}, {})

const Sidebar: React.FC = () => {
  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType)
    event.dataTransfer.effectAllowed = 'move'
  }

  return (
    <aside className='dnd-sidebar'>
      <div className='dnd-sidebar__header'>
        {SECTIONS['Input/Output'].map((kind) => {
          const node = NODES[kind]

          return (
            <div
              id={`dnd-node-${kind}`}
              key={kind}
              className='dnd-sidebar__node'
              onDragStart={(event) => onDragStart(event, kind)}
              draggable
            >
              <i className={`dnd-sidebar__icon fas fa-fw fa-lg ${node.icon}`}></i>
              <div className='flex flex-col'>
                <div className='flex items-center'>
                  <h4 className='dnd-sidebar__name'>{node.displayName}</h4>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {Object.keys(SECTIONS)
        .filter((section) => section != 'Input/Output')
        .map((section) => (
          <React.Fragment key={section}>
            <div className='active pad' data-controller='collapsable'>
              <h3 className='cursor-pointer' data-action='click->collapsable#toggle'>
                {section}
              </h3>

              <div
                className='collapsable flex flex-col max-h-0 overflow-hidden'
                data-collapsable-target='body'
                key={section}
              >
                {SECTIONS[section].map((kind) => {
                  const node = NODES[kind]

                  return (
                    <div
                      id={`dnd-node-${kind}`}
                      key={kind}
                      className='dnd-sidebar__node'
                      onDragStart={(event) => onDragStart(event, kind)}
                      draggable
                    >
                      <i className={`dnd-sidebar__icon fas fa-fw fa-lg ${node.icon}`}></i>
                      <div className='flex flex-col'>
                        <div className='flex items-center'>
                          <h4 className='dnd-sidebar__name'>{node.displayName}</h4>
                        </div>
                        <p className='dnd-sidebar__description'>{node.description}</p>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
            <hr />
          </React.Fragment>
        ))}
    </aside>
  )
}

export default Sidebar
