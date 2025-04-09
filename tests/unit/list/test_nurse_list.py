import unittest
from unittest.mock import Mock, PropertyMock, patch

from src import Request
from src.simulation.timed_object import PatientEvent, EventStatus, Plan, ReturnToOffice
from src.simulation.queue import NurseList


class TestNurseList(unittest.TestCase):
    def setUp(self):
        # print("setup called")
        self.mock_patient = Mock()
        self.mock_nurse = Mock()
        self.mock_nurse.speed = 1
        self.mock_graph = Mock()
        self.mock_sim_time = Mock()
        self.mock_sim_time.sim_time = 0

        self.event1 = PatientEvent(time=40, duration=10, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                   graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event2 = PatientEvent(time=90, duration=10, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                   graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.event3 = PatientEvent(time=170, duration=10, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                   graph=self.mock_graph, sim_time=self.mock_sim_time)

        self.nurse_list = NurseList([self.event3, self.event1, self.event2], self.mock_sim_time, self.mock_nurse, 20, self.mock_graph)
        self.empty_list = NurseList([], self.mock_sim_time, self.mock_nurse, 20, self.mock_graph)

    def test_init(self):
        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(self.event3, self.nurse_list.pop_front())

    def test_add_to_gap_front(self):
        new_event = PatientEvent(time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(new_event, self.nurse_list.front())
        self.assertEqual(0, new_event.time)

    def test_add_to_gap_middle(self):
        new_event = PatientEvent(time=0, duration=25, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(self.event3, self.nurse_list.pop_front())
        self.assertEqual(120, new_event.time)

    def test_add_to_gap_end(self):
        new_event = PatientEvent(time=0, duration=100, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_gap(new_event)

        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(self.event3, self.nurse_list.pop_front())
        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(200, new_event.time)



    def test_add_after_current_first(self):
        new_event = PatientEvent(time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)

       # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.PropertyMock
        with patch.object(type(self.event1), 'status', new_callable=PropertyMock, return_value=EventStatus.NOT_STARTED):
            self.nurse_list.add_after_current(new_event)

        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(0, new_event.time)
        self.assertEqual(40, self.event1.time)

    def test_add_after_current_second(self):
        new_event = PatientEvent(time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)

        with patch.object(type(self.event1), 'status', new_callable=PropertyMock, return_value=EventStatus.ACTIVE):
            self.nurse_list.add_after_current(new_event)

        self.assertEqual(self.event1, self.nurse_list.pop_front())
        self.assertEqual(new_event, self.nurse_list.pop_front())
        self.assertEqual(self.event2, self.nurse_list.pop_front())
        self.assertEqual(70, new_event.time)
        self.assertEqual(95, self.event2.time)
        self.assertEqual(170, self.event3.time)

    def test_add_after_current_pushback_all(self):
        new_event = PatientEvent(time=0, duration=100, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)

        with patch.object(type(self.event1), 'status', new_callable=PropertyMock, return_value=EventStatus.ACTIVE):
            self.nurse_list.add_after_current(new_event)

        self.assertEqual(40, self.nurse_list.pop_front().time)
        self.assertEqual(70, self.nurse_list.pop_front().time)
        self.assertEqual(190, self.nurse_list.pop_front().time)
        self.assertEqual(220, self.nurse_list.pop_front().time)

    def test_add_after_current_return_to_office(self):
        # add after current should be the same as add to start if current is return to office
        self.mock_sim_time.sim_time = 0.0  # gets set to start of return to office event
        return_event = ReturnToOffice(assigned_nurse=self.mock_nurse, graph=self.mock_graph,
                                      sim_time=self.mock_sim_time)
        nurse_list = NurseList([return_event, self.event2, self.event3], self.mock_sim_time, self.mock_nurse, 20,
                               self.mock_graph)

        return_event.pause = Mock()
        self.event2.pause = Mock()
        new_event = PatientEvent(time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        nurse_list.add_after_current(new_event)

    def test_add_to_start_no_pause(self):
        new_event = PatientEvent(time=0, duration=35, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        # self.event1.get_status = Mock(return_value=EventStatus.ACTIVE)
        self.nurse_list.add_to_start(new_event)

        self.assertEqual(0, self.nurse_list.pop_front().time)
        self.assertEqual(55, self.nurse_list.pop_front().time)
        self.assertEqual(90, self.nurse_list.pop_front().time)
        self.assertEqual(170, self.nurse_list.pop_front().time)

        self.assertEqual(EventStatus.NOT_STARTED, self.event1.status)

    def test_add_to_start_pause(self):
        new_event = PatientEvent(time=0, duration=45, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)

        self.event1.pause = Mock()
        with patch.object(type(self.event1), 'status', new_callable=PropertyMock, return_value=EventStatus.ACTIVE):
            self.nurse_list.add_to_start(new_event)

        self.event1.pause.assert_called_once()

    def test_add_to_start_return_to_office_new_event_fits(self):
        self.mock_sim_time.sim_time = 40.0  # gets set to start of return to office event
        return_event = ReturnToOffice(assigned_nurse=self.mock_nurse, graph=self.mock_graph,
                                      sim_time=self.mock_sim_time)
        nurse_list = NurseList([return_event, self.event2, self.event3], self.mock_sim_time, self.mock_nurse, 20,
                               self.mock_graph)
        self.mock_sim_time.sim_time = 0.0

        return_event.pause = Mock()
        self.event2.pause = Mock()
        new_event = PatientEvent(time=0, duration=5, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        nurse_list.add_to_start(new_event)

        # return event should be cancelled even if new event fits before it (although normally this won't even happen,
        # cause return to office is never scheduled for the future
        return_event.pause.assert_called_once()
        self.event2.pause.assert_not_called()
        self.assertEqual(new_event, nurse_list.pop_front())
        self.assertEqual(self.event2, nurse_list.pop_front())
        self.assertEqual(self.event3, nurse_list.pop_front())

    def test_add_to_start_return_to_office_new_event_fits_before_event2(self):
        self.mock_sim_time.sim_time = 0.0  # gets set to start of return to office event
        return_event = ReturnToOffice(assigned_nurse=self.mock_nurse, graph=self.mock_graph,
                                      sim_time=self.mock_sim_time)
        nurse_list = NurseList([return_event, self.event2, self.event3], self.mock_sim_time, self.mock_nurse, 20,
                               self.mock_graph)

        return_event.pause = Mock()
        self.event2.pause = Mock()
        new_event = PatientEvent(time=0, duration=20, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        nurse_list.add_to_start(new_event)

        # return event should be cancelled even if new event fits before it (although normally this won't even happen,
        # cause return to office is never scheduled for the future
        return_event.pause.assert_called_once()
        self.event2.pause.assert_not_called()
        self.assertEqual(new_event, nurse_list.pop_front())
        self.assertEqual(self.event2, nurse_list.pop_front())
        self.assertEqual(self.event3, nurse_list.pop_front())



    def test_add_to_start_return_to_office_event2_pushback(self):
        self.mock_sim_time.sim_time = 0.0  # gets set to start of return to office event
        return_event = ReturnToOffice(assigned_nurse=self.mock_nurse, graph=self.mock_graph,
                                      sim_time=self.mock_sim_time)
        nurse_list = NurseList([return_event, self.event2, self.event3], self.mock_sim_time, self.mock_nurse, 20,
                               self.mock_graph)

        return_event.pause = Mock()
        self.event2.pause = Mock()
        new_event = PatientEvent(time=0, duration=100, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        nurse_list.add_to_start(new_event)

        # return event should be cancelled even if new event fits before it (although normally this won't even happen,
        # cause return to office is never scheduled for the future

        return_event.pause.assert_called_once()
        self.event2.pause.assert_not_called()
        first_event = nurse_list.pop_front()
        second_event = nurse_list.pop_front()
        third_event = nurse_list.pop_front()

        self.assertEqual(new_event, first_event)
        self.assertEqual(0.0, first_event.time)
        self.assertEqual(self.event2, second_event)
        self.assertEqual(120, second_event.time)
        self.assertEqual(self.event3, third_event)
        self.assertEqual(170, third_event.time)

    def test_add_to_empty_list(self):
        new_event = PatientEvent(time=0, duration=100, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)

        self.empty_list.add_to_gap(new_event)
        self.assertEqual(new_event, self.empty_list.pop_front())

        self.empty_list.add_to_start(new_event)
        self.assertEqual(new_event, self.empty_list.pop_front())

        self.empty_list.add_after_current(new_event)
        self.assertEqual(new_event, self.empty_list.pop_front())

    def test_has_time_now(self):
        #event just about fits at start
        new_event = PatientEvent(time=0, duration=20, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.assertTrue(self.nurse_list.has_time_now(new_event))

        #event just about doesn't fit at start
        new_event = PatientEvent(time=0, duration=20.1, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.assertFalse(self.nurse_list.has_time_now(new_event))

        #event fits at start of empty list
        self.nurse_list.pop_front()
        self.nurse_list.pop_front()
        self.nurse_list.pop_front()
        self.assertTrue(self.nurse_list.has_time_now(new_event))

    def test_current_event_level(self):
        #patient event has level -1
        self.assertEqual(-1, self.nurse_list.current_event_level())

        #inactive request returns level -1
        request = Request(time=0, duration=5, patient=self.mock_patient, level=2,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_start(request)
        self.assertEqual(-1, self.nurse_list.current_event_level())

        #active request has level of request
        with patch.object(type(request), 'status', new_callable=PropertyMock, return_value=EventStatus.ACTIVE):
            self.assertEqual(2, self.nurse_list.current_event_level())

        #plan has level -1
        plan = Plan(time=0, duration=5, patient=self.mock_patient, nurse=self.mock_nurse,
                          graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.nurse_list.add_to_start(plan)
        with patch.object(type(plan), 'status', new_callable=PropertyMock, return_value=EventStatus.ACTIVE):
            self.assertEqual(-1, self.nurse_list.current_event_level())

    def test_run_next_step_empty_list(self):
        """Test running next step on empty list raises exception"""
        with self.assertRaises(Exception) as context:
            self.empty_list.run_next_step()
        self.assertTrue("can't run next step of emtpy list" in str(context.exception))

    def test_run_next_step_event_not_finished(self):
        """Test running next step when event is not finished"""
        # Mock event1's run_next_step to return False (not finished)
        self.event1.run_next_step = Mock()
        self.event1.run_next_step.return_value = False

        # Run next step
        result = self.nurse_list.run_next_step()

        # Verify results
        self.assertFalse(result)  # Method should return False
        self.event1.run_next_step.assert_called_once()  # Event's run_next_step should be called
        self.assertEqual(self.event1, self.nurse_list.front())  # Event should still be at front
        self.assertEqual([], self.nurse_list.event_logs)  # No logs should be added

    def test_run_next_step_event_finished(self):
        """Test running next step when event is finished"""
        # Mock event1's run_next_step to return True (finished)
        self.event1.run_next_step = Mock()
        self.event1.run_next_step.return_value = True
        self.mock_sim_time.sim_time = 51 #not enough time to return to office before next event

        # Run next step
        result = self.nurse_list.run_next_step()

        # Verify results
        self.assertTrue(result)  # Method should return True
        self.event1.run_next_step.assert_called_once()  # Event's run_next_step should be called
        self.assertEqual(self.event2, self.nurse_list.front())  # Next event should now be at front
        self.assertEqual(self.event1.log, self.nurse_list.event_logs)  # Log should be added

    # -------------- RETURN TO OFFICE TESTS --------------
    def test_run_next_step_create_return_to_office(self):
        """Test return to office event creation when conditions are met"""
        self.event1.run_next_step = Mock()
        self.event1.run_next_step.return_value = True

        # Run next step
        self.nurse_list.run_next_step()

        # Verify return to office event was created
        current_front = self.nurse_list.front()
        self.assertEqual(current_front.type, 'return_to_office')
        self.assertEqual(current_front.time, self.mock_sim_time.sim_time)

    def test_run_next_step_no_return_to_office_when_in_office(self):
        """Test no return to office event is created when nurse is already in office"""
        # Setup conditions where nurse is already in office
        self.event1.run_next_step = Mock()
        self.event1.run_next_step.return_value = True
        self.mock_office = Mock()
        self.mock_nurse.pos = self.mock_office
        self.mock_graph.nurse_office = self.mock_office

        # Run next step
        self.nurse_list.run_next_step()

        # Verify next event is event2, not a return to office event
        self.assertEqual(self.nurse_list.front(), self.event2)


    def test_has_time_now_return_to_office(self):
        self.mock_sim_time.sim_time = 40.0 #gets set to start of return to office event
        return_event = ReturnToOffice(assigned_nurse=self.mock_nurse, graph=self.mock_graph, sim_time=self.mock_sim_time)
        nurse_list = NurseList([return_event, self.event2, self.event3], self.mock_sim_time, self.mock_nurse, 20, self.mock_graph)
        self.mock_sim_time.sim_time = 0.0


        # event normally wouldn't fit, but will if return to office doesn't count
        new_event = PatientEvent(time=0, duration=50, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.assertEqual(nurse_list.has_time_now(new_event), True)

        # if there's not enough time until the event after return to office, it still returns false
        new_event = PatientEvent(time=0, duration=80, patient=self.mock_patient, assigned_nurse=self.mock_nurse,
                                 graph=self.mock_graph, sim_time=self.mock_sim_time)
        self.assertEqual(nurse_list.has_time_now(new_event), False)






if __name__ == "__main__":
    unittest.main()

