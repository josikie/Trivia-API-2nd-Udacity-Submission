import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null
    };
  }

  paginated = ''
  componentDidMount() {
    this.getQuestions();
  }


  getQuestions = () => {
    $.ajax({
      url: `/api/questions?page=${this.state.page}`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.paginated = 'paginated'
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  selectPage(num) {
    this.setState({ page: num }, () => this.getQuestions());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    if(this.paginated === 'paginated'){
      for (let i = 1; i <= maxPage; i++) {
        pageNumbers.push(
          <span
            key={i}
            className={`page-num ${i === this.state.page ? 'active' : ''}`}
            onClick={() => {
              this.selectPage(i);
            }}
            >
            {i}
          </span>
        );
      }
    }else if(this.paginated === 'search'){
      console.log(this.paginated)
    }else{
      console.log(this.paginated)
    }
    return pageNumbers;
  }

  getByCategory = (id) => {
    $.ajax({
      url: `/api/categories/${id}/questions`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.paginated = 'category'
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/api/questions`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ searchTerm: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.paginated = 'search'
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('Are you sure you want to delete the question?\n\nNote: After you click one of the buttons, You will redirect to the main page. Don\'t worry if you feel something different, because the data appear different in the main page (There is noting wrong).')) {
        $.ajax({
          url: `/api/questions/${id}`, //TODO: update request URL
          type: 'DELETE',
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again');
            return;
          },
        });
      }
    }
  };

  render() {
    return (
      <div className='question-view'>
        <div className='categories-list'>
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            {Object.keys(this.state.categories).map((id) => (
              <li
                key={id}
                onClick={() => {
                  this.getByCategory(id);
                }}
              >
                {this.state.categories[id]}
                <img
                  className='category'
                  alt={`${this.state.categories[id]}`}
                  src={`${this.state.categories[id]}.svg`}
                />
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch} />
        </div>
        <div className='questions-list'>
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category]}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          
          <div className='pagination-menu'>{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
