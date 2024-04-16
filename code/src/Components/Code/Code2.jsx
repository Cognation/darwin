import React from 'react'
import ReactTextFormat from 'react-text-format';

function Code2() {
    const text = `**OpenAl Whisper Research Paper Overview**
    **Introduction:**
    OpenAl introduced a neural network named Whisper, designed to significantly enhance the robustness and accuracy of English speech recognition. Whisper marks a step towards achieving human-level performance in automatic speech recognition (ASR) systems. Its development emphasizes the utility of large, diverse datasets in training more capable and versatile models.
    **Dataset and Training:**
    Whisper was trained on an extensive dataset consisting of 680,000 hours of multilingual audio encompassing a variety of tasks, sourced from the web. This massive, diverse training set ensures Whisper's improved performance in dealing with accents, background noises, technical language, and simultaneously enables it to transcribe and translate multiple languages into English. The choice to open-source both the models and the inference code aims to provide a solid foundation for future research and the creation of practical applications in robust speech processing.
    **Architecture:**
    The architecture of Whisper is based on a straightforward end-to-end approach,`;;


  return (
    <div style={{marginTop:"60px" , marginLeft:"20px" , marginRight:"20px"}} >
        <p dangerouslySetInnerHTML={{ __html: text }} />

      
    </div>
  )
}

export default Code2
