import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JoinCourseComponent } from './join-course.component';

describe('JoinCourseComponent', () => {
  let component: JoinCourseComponent;
  let fixture: ComponentFixture<JoinCourseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JoinCourseComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(JoinCourseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
